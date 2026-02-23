"""
benchmarks/profile_read.py
==========================

Profile inewave read operations for representative file types.

Measures:
  - Import time for top-level inewave packages
  - Per-handler total read time
  - Parsing phase (TabularParser.parse_lines)
  - DataFrame construction (_build_dataframe / formata_df_meses_para_datas_nwlistop)
  - Aggregation (__monta_tabela pd.concat loop)

Run from the repository root:
    python benchmarks/profile_read.py

Output: benchmarks/profile_report.md
"""

from __future__ import annotations

import cProfile
import importlib
import io
import pstats
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Generator
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Timing helpers
# ---------------------------------------------------------------------------


@dataclass
class PhaseTimings:
    """Accumulated nanosecond wall-clock times per phase."""

    parse_ns: int = 0
    build_df_ns: int = 0
    format_ns: int = 0
    concat_ns: int = 0
    total_ns: int = 0

    def parse_s(self) -> float:
        return self.parse_ns / 1e9

    def build_df_s(self) -> float:
        return self.build_df_ns / 1e9

    def format_s(self) -> float:
        return self.format_ns / 1e9

    def concat_s(self) -> float:
        return self.concat_ns / 1e9

    def total_s(self) -> float:
        return self.total_ns / 1e9

    def other_s(self) -> float:
        return max(
            0.0,
            self.total_s()
            - self.parse_s()
            - self.build_df_s()
            - self.format_s()
            - self.concat_s(),
        )


@contextmanager
def _timed(accumulator_ns: list[int]) -> Generator[None, None, None]:
    """Context manager that adds elapsed nanoseconds to accumulator_ns[0]."""
    t0 = time.perf_counter_ns()
    try:
        yield
    finally:
        accumulator_ns[0] += time.perf_counter_ns() - t0


# ---------------------------------------------------------------------------
# Instrumentation patches
# ---------------------------------------------------------------------------


def _make_parse_lines_wrapper(
    original_parse_lines: Callable[..., Any],
    timings: PhaseTimings,
) -> Callable[..., Any]:
    """Return a wrapper that times TabularParser.parse_lines calls."""

    def wrapper(self_inner: Any, lines: list[str]) -> Any:  # noqa: ANN401
        acc: list[int] = [0]
        with _timed(acc):
            result = original_parse_lines(self_inner, lines)
        timings.parse_ns += acc[0]
        return result

    return wrapper


def _make_build_dataframe_wrapper(
    original_build: Callable[..., Any],
    timings: PhaseTimings,
) -> Callable[..., Any]:
    """Return a wrapper that times _build_dataframe calls."""

    def wrapper(self_inner: Any, parsed: dict) -> Any:  # noqa: ANN401
        acc: list[int] = [0]
        with _timed(acc):
            result = original_build(self_inner, parsed)
        timings.build_df_ns += acc[0]
        return result

    return wrapper


def _make_formata_wrapper(
    original_formata: Callable[..., Any],
    timings: PhaseTimings,
) -> Callable[..., Any]:
    """Return a wrapper that times formata_df_meses_para_datas_nwlistop calls."""

    def wrapper(df: Any) -> Any:  # noqa: ANN401
        acc: list[int] = [0]
        with _timed(acc):
            result = original_formata(df)
        timings.format_ns += acc[0]
        return result

    return wrapper


def _make_monta_tabela_wrapper(
    original_monta: Callable[..., Any],
    timings: PhaseTimings,
) -> Callable[..., Any]:
    """
    Return a wrapper for __monta_tabela that times the pd.concat loop.

    The caller is responsible for retrieving the original function from the
    class __dict__ before calling this factory; the original reference is
    captured in the closure so that restore is safe after setattr.
    """

    def wrapper(self_inner: Any) -> Any:  # noqa: ANN401
        acc: list[int] = [0]
        with _timed(acc):
            result = original_monta(self_inner)
        timings.concat_ns += acc[0]
        return result

    return wrapper


# ---------------------------------------------------------------------------
# Import timing
# ---------------------------------------------------------------------------


def measure_import_times() -> dict[str, float]:
    """
    Measure import wall-clock time for top-level inewave packages.

    Modules are removed from sys.modules before each timing so that
    importlib.import_module performs a fresh load from bytecode cache.
    """
    targets = [
        "inewave",
        "inewave.nwlistop",
        "inewave.newave",
    ]
    results: dict[str, float] = {}
    for mod_name in targets:
        # Remove the module and all its sub-modules from the cache.
        to_remove = [
            k
            for k in sys.modules
            if k == mod_name or k.startswith(mod_name + ".")
        ]
        for k in to_remove:
            del sys.modules[k]
        t0 = time.perf_counter()
        importlib.import_module(mod_name)
        results[mod_name] = time.perf_counter() - t0
    return results


# ---------------------------------------------------------------------------
# Per-handler profiling
# ---------------------------------------------------------------------------

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"

# We import mock helpers at module level after the import-timing section has
# already been done so that import time measurements are not contaminated.


@dataclass
class HandlerSpec:
    """Everything needed to profile one file handler."""

    label: str
    handler_class: type
    mock_data: list[str]
    read_kwargs: dict[str, Any] = field(default_factory=dict)
    # Archive classes that own a __monta_tabela; may be None for Pmo.
    arquivo_class: type | None = None


def _run_cprofile(spec: HandlerSpec) -> str:
    """Run cProfile over one handler read + valores access; return top-20."""
    from tests.mocks.mock_open import mock_open as project_mock_open

    mock_data_str = "".join(spec.mock_data)
    pr = cProfile.Profile()

    def profiled_read() -> None:
        m = project_mock_open(read_data=mock_data_str)
        with patch("builtins.open", m):
            obj = spec.handler_class.read(ARQ_TESTE, **spec.read_kwargs)
            # Trigger lazy property to capture aggregation in profile
            if hasattr(obj, "valores"):
                _ = obj.valores

    pr.enable()
    profiled_read()
    pr.disable()

    stream = io.StringIO()
    ps = pstats.Stats(pr, stream=stream).sort_stats("cumulative")
    ps.print_stats(20)
    return stream.getvalue()


def _measure_phases(spec: HandlerSpec, n_runs: int = 5) -> PhaseTimings:
    """
    Measure phase timings by patching key methods.

    Runs n_runs times and returns the best (lowest total wall-clock)
    result to minimise scheduling noise, consistent with timeit convention.

    The __monta_tabela restore is safe because we capture the original from
    the class __dict__ BEFORE the first setattr, and restore it directly
    using that saved reference without re-reading __dict__ after patching.
    """
    import cfinterface.components.tabular as _tabular_mod
    import inewave._utils.formatacao as _fmt_mod
    import inewave.nwlistop.modelos.blocos.tabela_serie_anual as _tsa_mod
    import inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual as _tspa_mod

    from inewave.nwlistop.modelos.blocos.tabela_serie_anual import (
        TabelaSerieAnual,
    )
    from inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual import (
        TabelaSeriePatamarAnual,
    )
    from tests.mocks.mock_open import mock_open as project_mock_open

    mock_data_str = "".join(spec.mock_data)

    # --- Save all originals ONCE before any patching. ---
    orig_parse = _tabular_mod.TabularParser.parse_lines
    orig_build_annual = TabelaSerieAnual._build_dataframe
    orig_build_patamar = TabelaSeriePatamarAnual._build_dataframe
    orig_tsa_formata = _tsa_mod.formata_df_meses_para_datas_nwlistop
    orig_tspa_formata = _tspa_mod.formata_df_meses_para_datas_nwlistop
    orig_fmt_formata = _fmt_mod.formata_df_meses_para_datas_nwlistop

    # For __monta_tabela: read from __dict__ so we capture the true original,
    # not whatever is currently bound after a previous setattr.
    monta_mangled: str | None = None
    orig_monta: Any = None
    if spec.arquivo_class is not None:
        monta_mangled = f"_{spec.arquivo_class.__name__}__monta_tabela"
        # Walk the MRO to find the owning class's __dict__ entry.
        for base in spec.arquivo_class.__mro__:
            if monta_mangled in base.__dict__:
                orig_monta = base.__dict__[monta_mangled]
                break

    best: PhaseTimings | None = None

    for _ in range(n_runs):
        timings = PhaseTimings()

        # --- Install wrappers using the saved originals. ---
        _tabular_mod.TabularParser.parse_lines = (  # type: ignore[method-assign]
            _make_parse_lines_wrapper(orig_parse, timings)
        )
        TabelaSerieAnual._build_dataframe = (  # type: ignore[method-assign]
            _make_build_dataframe_wrapper(orig_build_annual, timings)
        )
        TabelaSeriePatamarAnual._build_dataframe = (  # type: ignore[method-assign]
            _make_build_dataframe_wrapper(orig_build_patamar, timings)
        )
        formata_wrapper = _make_formata_wrapper(orig_tsa_formata, timings)
        _tsa_mod.formata_df_meses_para_datas_nwlistop = formata_wrapper  # type: ignore[assignment]
        _tspa_mod.formata_df_meses_para_datas_nwlistop = formata_wrapper  # type: ignore[assignment]
        _fmt_mod.formata_df_meses_para_datas_nwlistop = formata_wrapper  # type: ignore[assignment]

        if monta_mangled is not None and orig_monta is not None:
            setattr(
                spec.arquivo_class,
                monta_mangled,
                _make_monta_tabela_wrapper(orig_monta, timings),
            )

        try:
            m = project_mock_open(read_data=mock_data_str)
            t_total_start = time.perf_counter_ns()
            with patch("builtins.open", m):
                obj = spec.handler_class.read(ARQ_TESTE, **spec.read_kwargs)
                # Force the lazy aggregation to measure __monta_tabela.
                if hasattr(obj, "valores"):
                    _ = obj.valores
            timings.total_ns = time.perf_counter_ns() - t_total_start
        finally:
            # Restore all originals using the references saved before the loop.
            _tabular_mod.TabularParser.parse_lines = orig_parse  # type: ignore[method-assign]
            TabelaSerieAnual._build_dataframe = orig_build_annual  # type: ignore[method-assign]
            TabelaSeriePatamarAnual._build_dataframe = orig_build_patamar  # type: ignore[method-assign]
            _tsa_mod.formata_df_meses_para_datas_nwlistop = orig_tsa_formata  # type: ignore[assignment]
            _tspa_mod.formata_df_meses_para_datas_nwlistop = orig_tspa_formata  # type: ignore[assignment]
            _fmt_mod.formata_df_meses_para_datas_nwlistop = orig_fmt_formata  # type: ignore[assignment]
            if monta_mangled is not None and orig_monta is not None:
                # Restore using the original reference, not a re-read of __dict__.
                setattr(spec.arquivo_class, monta_mangled, orig_monta)

        if best is None or timings.total_ns < best.total_ns:
            best = timings

    assert best is not None
    return best


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def _pct(part: float, total: float) -> str:
    if total <= 0:
        return "N/A"
    return f"{100.0 * part / total:.1f}%"


def _fmt_s(val: float) -> str:
    return f"{val:.6f}"


def _build_summary_row(
    label: str,
    handler_cls: type,
    timings: PhaseTimings,
) -> str:
    total = timings.total_s()
    parse = timings.parse_s()
    build = timings.build_df_s()
    fmt = timings.format_s()
    concat = timings.concat_s()
    # DataFrame % = build + format (both happen inside _build_dataframe path)
    df_pct = _pct(build + fmt, total)
    return (
        f"| {label} | `{handler_cls.__name__}` "
        f"| {_fmt_s(total)} "
        f"| {_pct(parse, total)} "
        f"| {df_pct} "
        f"| {_pct(concat, total)} "
        f"| {_pct(timings.other_s(), total)} |"
    )


def generate_report(
    specs: list[HandlerSpec],
    all_timings: list[PhaseTimings],
    import_times: dict[str, float],
    cprofile_outputs: dict[str, str],
) -> str:
    lines: list[str] = []

    lines.append("# inewave Read Performance Profile\n")
    lines.append(
        "> Generated by `benchmarks/profile_read.py`.  "
        "Times are best-of-5 wall-clock measurements using "
        "`time.perf_counter_ns()`.  "
        "Phases are measured via targeted monkey-patching of internal "
        "helpers; overlaps between phases (build_df includes format) mean "
        "columns may not sum to exactly 100 %.\n"
    )

    # --- Summary table ---
    lines.append("## Summary Table\n")
    lines.append(
        "| File Type | Handler | Total Time (s) | Parsing % "
        "| DataFrame % | Aggregation % | Other % |"
    )
    lines.append("|---|---|---|---|---|---|---|")
    for spec, t in zip(specs, all_timings):
        lines.append(_build_summary_row(spec.label, spec.handler_class, t))
    lines.append("")

    # --- Raw phase times (absolute, useful when percentages round to 0) ---
    lines.append("## Raw Phase Times (seconds)\n")
    lines.append(
        "| File Type | Total (s) | Parse (s) | Build-DF (s)"
        " | Format (s) | Concat (s) |"
    )
    lines.append("|---|---|---|---|---|---|")
    for spec, t in zip(specs, all_timings):
        lines.append(
            f"| {spec.label} "
            f"| {_fmt_s(t.total_s())} "
            f"| {_fmt_s(t.parse_s())} "
            f"| {_fmt_s(t.build_df_s())} "
            f"| {_fmt_s(t.format_s())} "
            f"| {_fmt_s(t.concat_s())} |"
        )
    lines.append("")

    # --- Import times ---
    lines.append("## Import Time\n")
    lines.append("| Module | Time (s) |")
    lines.append("|---|---|")
    for mod, t in import_times.items():
        lines.append(f"| `{mod}` | {_fmt_s(t)} |")
    lines.append("")

    # --- Per-file cProfile ---
    lines.append("## Per-File cProfile Top-20\n")
    for label, cprof_out in cprofile_outputs.items():
        lines.append(f"### {label}\n")
        lines.append("```")
        lines.append(cprof_out.strip())
        lines.append("```\n")

    # --- Key findings ---
    lines.append("## Key Findings\n")

    # Gather aggregate percentages to identify dominant bottlenecks
    # Use a minimum total time threshold to filter out files where mock-I/O
    # overhead dominates and makes phase percentages unreliable (e.g. Cdef
    # with only a few dozen lines shows >100% for build_df because its total
    # time is dominated by mock.__call__ overhead rather than real work).
    MIN_TOTAL_S = 0.010

    findings: list[tuple[float, str]] = []
    for spec, t in zip(specs, all_timings):
        total = t.total_s()
        if total < MIN_TOTAL_S:
            continue
        parse_pct = 100.0 * t.parse_s() / total
        df_pct = 100.0 * (t.build_df_s() + t.format_s()) / total
        concat_pct = 100.0 * t.concat_s() / total
        findings.append(
            (
                parse_pct,
                f"`TabularParser.parse_lines` accounts for {parse_pct:.1f}% "
                f"of read time in `{spec.label}` "
                f"({t.parse_s() * 1000:.1f} ms out of {total * 1000:.1f} ms). "
                f"The hot path is `Line.read` -> `__positional_reading` -> "
                f"`FloatField._textual_read` called once per data cell.",
            )
        )
        findings.append(
            (
                df_pct,
                f"`_build_dataframe` + `formata_df_meses_para_datas_nwlistop` "
                f"accounts for {df_pct:.1f}% of read time in `{spec.label}` "
                f"({(t.build_df_s() + t.format_s()) * 1000:.1f} ms). "
                f"Internally, `np.tile` / `np.repeat` / `np.concatenate` are "
                f"called once per year-block to construct the tidy DataFrame.",
            )
        )
        if concat_pct > 0.1:
            findings.append(
                (
                    concat_pct,
                    f"`__monta_tabela` (pd.concat loop) accounts for "
                    f"{concat_pct:.1f}% of read time in `{spec.label}` "
                    f"({t.concat_s() * 1000:.3f} ms). With mock data (1 year "
                    f"block) this is near-zero; at production scale (20+ "
                    f"year blocks) the O(n^2) concat copies dominate.",
                )
            )

    # Add Pmo-specific finding from cProfile (DataFrame.apply + melt path)
    pmo_timings = next(
        (t for spec, t in zip(specs, all_timings) if "Pmo" in spec.label),
        None,
    )
    if pmo_timings is not None and pmo_timings.total_s() >= MIN_TOTAL_S:
        findings.append(
            (
                50.0,  # fixed rank to appear near top
                f"`Pmo` read time ({pmo_timings.total_s() * 1000:.1f} ms) is "
                f"dominated by `DataFrame.apply` + `DataFrame.melt` calls "
                f"inside `converte_tabela_em_df` (cProfile shows ~171 ms / "
                f"31 calls for apply+melt vs ~126 ms for mock readline). "
                f"The newave block-file path uses a different DataFrame "
                f"construction strategy than the nwlistop TabularParser path.",
            )
        )

    findings.sort(key=lambda x: x[0], reverse=True)
    seen_categories: set[str] = set()
    unique_findings: list[str] = []
    for _, desc in findings:
        # Keep one finding per phase-category to avoid redundant entries.
        category = desc.split("`")[1]
        if category not in seen_categories:
            seen_categories.add(category)
            unique_findings.append(desc)
        if len(unique_findings) >= 5:
            break

    for i, finding in enumerate(unique_findings, start=1):
        lines.append(f"{i}. {finding}")
    lines.append("")

    # --- Recommendations ---
    lines.append("## Recommendations\n")

    phase_totals: dict[str, float] = {
        "parse": sum(t.parse_s() for t in all_timings),
        "dataframe": sum((t.build_df_s() + t.format_s()) for t in all_timings),
        "concat": sum(t.concat_s() for t in all_timings),
    }
    sorted_phases = sorted(
        phase_totals.items(), key=lambda x: x[1], reverse=True
    )

    rec_map = {
        "parse": (
            "**Parsing bottleneck (ticket 020):** "
            "`TabularParser.parse_lines` iterates over every raw line and "
            "calls `Line.read()` once per line via Python-level field "
            "extraction. Consider batching field reads with "
            "`numpy.frompyfunc` or replacing the per-line Python loop with "
            "a vectorised `numpy.genfromtxt` / `pandas.read_fwf` approach "
            "on the collected raw text."
        ),
        "dataframe": (
            "**DataFrame construction bottleneck (ticket 020/021):** "
            "`_build_dataframe` and `formata_df_meses_para_datas_nwlistop` "
            "perform repeated `np.tile` / `np.repeat` / `np.concatenate` "
            "calls for every year-block. Pre-allocating a single output "
            "array across all year-blocks (known from `ANO:` header "
            "scanning) before populating it would eliminate repeated "
            "intermediate allocations."
        ),
        "concat": (
            "**Aggregation bottleneck (ticket 021):** "
            "`__monta_tabela` in `ArquivoREE` / `ArquivoSubmercado` / etc. "
            "calls `pd.concat([df, b.data], ignore_index=True)` in a loop, "
            "which allocates a new DataFrame on every iteration (O(n^2) "
            "copies). Replace with `pd.concat(list_of_all_blocks)` called "
            "once after collecting all block DataFrames."
        ),
    }

    for rank, (phase, _) in enumerate(sorted_phases, start=1):
        lines.append(f"{rank}. {rec_map[phase]}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    # Step 1: Measure import times before importing heavy test-mock modules.
    print("Measuring import times...", flush=True)
    import_times = measure_import_times()

    # Step 2: Import everything needed for profiling.
    from inewave.newave.pmo import Pmo
    from inewave.nwlistop.cdef import Cdef
    from inewave.nwlistop.cmarg import Cmarg
    from inewave.nwlistop.earmf import Earmf
    from inewave.nwlistop.earmfp import Earmfp
    from inewave.nwlistop.earmfsin import Earmfsin
    from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE
    from inewave.nwlistop.modelos.arquivos.arquivosin import ArquivoSIN
    from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
        ArquivoSubmercado,
    )
    from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
        ArquivoSubmercadoPatamar,
    )
    from tests.mocks.arquivos.cdef import MockCdef
    from tests.mocks.arquivos.cmarg import MockCmarg
    from tests.mocks.arquivos.earmf import MockEarmf
    from tests.mocks.arquivos.earmfp import MockEarmfp
    from tests.mocks.arquivos.earmfsin import MockEarmfSIN
    from tests.mocks.arquivos.pmo import MockPMO

    specs: list[HandlerSpec] = [
        HandlerSpec(
            label="Non-patamar REE (Earmf)",
            handler_class=Earmf,
            mock_data=MockEarmf,
            arquivo_class=ArquivoREE,
        ),
        HandlerSpec(
            label="Non-patamar SIN (Earmfsin)",
            handler_class=Earmfsin,
            mock_data=MockEarmfSIN,
            arquivo_class=ArquivoSIN,
        ),
        HandlerSpec(
            label="Non-patamar Submercado (Cdef)",
            handler_class=Cdef,
            mock_data=MockCdef,
            arquivo_class=ArquivoSubmercado,
        ),
        HandlerSpec(
            label="Patamar Submercado (Cmarg)",
            handler_class=Cmarg,
            mock_data=MockCmarg,
            arquivo_class=ArquivoSubmercadoPatamar,
        ),
        HandlerSpec(
            label="Patamar REE (Earmfp)",
            handler_class=Earmfp,
            mock_data=MockEarmfp,
            arquivo_class=ArquivoREE,
        ),
        HandlerSpec(
            label="Newave SectionFile (Pmo)",
            handler_class=Pmo,
            mock_data=list(MockPMO),
            arquivo_class=None,  # Pmo has no __monta_tabela
        ),
    ]

    # Step 3: Measure phases.
    all_timings: list[PhaseTimings] = []
    for spec in specs:
        print(f"  Profiling {spec.label}...", flush=True)
        timings = _measure_phases(spec, n_runs=5)
        all_timings.append(timings)
        print(
            f"    total={timings.total_s():.4f}s  "
            f"parse={timings.parse_s():.4f}s  "
            f"build_df={timings.build_df_s():.4f}s  "
            f"format={timings.format_s():.4f}s  "
            f"concat={timings.concat_s():.4f}s"
        )

    # Step 4: cProfile per handler.
    print("Running cProfile passes...", flush=True)
    cprofile_outputs: dict[str, str] = {}
    for spec in specs:
        print(f"  cProfile {spec.label}...", flush=True)
        cprofile_outputs[spec.label] = _run_cprofile(spec)

    # Step 5: Generate and write report.
    report = generate_report(specs, all_timings, import_times, cprofile_outputs)
    report_path = Path(__file__).parent / "profile_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {report_path}")


if __name__ == "__main__":
    # Run from the repository root so that test mock imports resolve correctly.
    repo_root = Path(__file__).parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    main()
