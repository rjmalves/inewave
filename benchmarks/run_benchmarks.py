"""
benchmarks/run_benchmarks.py
============================

Entry point for the inewave benchmark suite.

Usage::

    python benchmarks/run_benchmarks.py [--iterations N]

Default iterations: 10.  Writes ``benchmarks/benchmark_results.md``.

On the second run (when a previous results file exists) a delta % column
is added to each table so regressions and improvements are immediately
visible.
"""

from __future__ import annotations

import argparse
import platform
import re
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from benchmarks.bench_import import run_all_import_benchmarks  # noqa: E402
from benchmarks.bench_read import (  # noqa: E402
    BenchmarkResult,
    run_all_aggregation_benchmarks,
    run_all_read_benchmarks,
    run_hidr_benchmark,
)

_REPORT_PATH = Path(__file__).parent / "benchmark_results.md"


def _parse_previous_means(report_text: str) -> dict[str, float]:
    """
    Extract benchmark-name -> mean-time mapping from a previous markdown
    report.

    Parses rows of the form::

        | name | 0.1234 | ...

    Only rows inside the three recognised benchmark tables are parsed.
    Returns an empty dict if nothing can be parsed.
    """
    means: dict[str, float] = {}
    # Each table row: | name | mean | ...  (name is never empty for data rows)
    row_re = re.compile(
        r"^\|\s*(?P<name>[^|]+?)\s*\|\s*(?P<mean>\d+\.\d+)\s*\|"
    )
    for line in report_text.splitlines():
        m = row_re.match(line)
        if m:
            name = m.group("name").strip()
            # Skip header rows and separator rows.
            if name.lower() in {"benchmark", "---", ""}:
                continue
            try:
                means[name] = float(m.group("mean"))
            except ValueError:
                pass
    return means


def _delta_str(current: float, previous: float | None) -> str:
    """Return a percentage delta string or empty string when unavailable."""
    if previous is None or previous <= 0.0:
        return ""
    pct = 100.0 * (current - previous) / previous
    sign = "+" if pct > 0 else ""
    return f"{sign}{pct:.1f}%"


def _format_memory(mb: float) -> str:
    """Format memory value; return 'N/A' for sentinel (negative) values."""
    if mb < 0:
        return "N/A"
    return f"{mb:.2f}"


def _build_table(
    results: list[BenchmarkResult | str],
    previous_means: dict[str, float],
    has_previous: bool,
) -> list[str]:
    """
    Build a markdown table from a list of BenchmarkResult (or SKIPPED strings).

    Parameters
    ----------
    results:
        Benchmark results — each entry is either a `BenchmarkResult` or a
        plain string starting with the benchmark name followed by
        " SKIPPED: ...".
    previous_means:
        Parsed mean times from the previous run.  May be empty.
    has_previous:
        Whether a previous results file was successfully loaded.  Controls
        whether the Delta column is shown.

    Returns
    -------
    List of markdown lines forming the table.
    """
    if has_previous:
        header = (
            "| Benchmark | Mean (s) | Delta | Median (s) | Min (s) | Max (s)"
            " | Std Dev (s) | Peak Memory (MB) |"
        )
        separator = "|-----------|----------|-------|------------|---------|---------|-------------|------------------|"
    else:
        header = (
            "| Benchmark | Mean (s) | Median (s) | Min (s) | Max (s)"
            " | Std Dev (s) | Peak Memory (MB) |"
        )
        separator = "|-----------|----------|------------|---------|---------|-------------|------------------|"

    lines = [header, separator]

    for entry in results:
        if isinstance(entry, str):
            # SKIPPED entry — extract the name part before " SKIPPED:"
            parts = entry.split(" SKIPPED:", 1)
            skipped_name = parts[0].strip()
            reason = parts[1].strip() if len(parts) > 1 else ""
            skipped_label = f"SKIPPED: {reason}" if reason else "SKIPPED"
            if has_previous:
                lines.append(
                    f"| {skipped_name} | {skipped_label} | — | — | — | — | — | — |"
                )
            else:
                lines.append(
                    f"| {skipped_name} | {skipped_label} | — | — | — | — | — |"
                )
            continue

        # Successful BenchmarkResult
        prev = previous_means.get(entry.name)
        mean = entry.mean()
        delta = _delta_str(mean, prev) if has_previous else None
        memory = _format_memory(entry.peak_memory_mb)

        if has_previous:
            lines.append(
                f"| {entry.name} "
                f"| {mean:.4f} "
                f"| {delta} "
                f"| {entry.median():.4f} "
                f"| {entry.min():.4f} "
                f"| {entry.max():.4f} "
                f"| {entry.stdev():.4f} "
                f"| {memory} |"
            )
        else:
            lines.append(
                f"| {entry.name} "
                f"| {mean:.4f} "
                f"| {entry.median():.4f} "
                f"| {entry.min():.4f} "
                f"| {entry.max():.4f} "
                f"| {entry.stdev():.4f} "
                f"| {memory} |"
            )

    return lines


def generate_report(
    import_results: list[BenchmarkResult | str],
    read_results: list[BenchmarkResult | str],
    aggregation_results: list[BenchmarkResult | str],
    iterations: int,
    previous_means: dict[str, float],
    has_previous: bool,
) -> str:
    """
    Assemble the full markdown benchmark report.

    Parameters
    ----------
    import_results:
        Results from import benchmarks.
    read_results:
        Results from read benchmarks.
    aggregation_results:
        Results from aggregation / specialised benchmarks (e.g. Hidr).
    iterations:
        Number of iterations used in this run.
    previous_means:
        Parsed mean times from the previous run.
    has_previous:
        Whether a valid previous file was found.

    Returns
    -------
    The complete markdown document as a string.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    python_ver = sys.version.replace("\n", " ")
    plat = platform.platform()
    cpu = platform.processor() or platform.machine()

    lines: list[str] = [
        "# inewave Benchmark Results",
        "",
        f"Generated: {timestamp}  ",
        f"Python: {python_ver}  ",
        f"Platform: {plat}  ",
        f"CPU: {cpu}  ",
        f"Iterations: {iterations}",
        "",
        "Note: Memory measurements use tracemalloc (Python-level allocations only).",
        "",
    ]

    lines.append("## Import Benchmarks")
    lines.append("")
    lines.extend(_build_table(import_results, previous_means, has_previous))
    lines.append("")

    lines.append("## Read Benchmarks")
    lines.append("")
    lines.extend(_build_table(read_results, previous_means, has_previous))
    lines.append("")

    lines.append("## Aggregation Benchmarks")
    lines.append("")
    lines.extend(
        _build_table(aggregation_results, previous_means, has_previous)
    )
    lines.append("")

    return "\n".join(lines)


def _print_summary(
    import_results: list[BenchmarkResult | str],
    read_results: list[BenchmarkResult | str],
    aggregation_results: list[BenchmarkResult | str],
    has_previous: bool,
    previous_means: dict[str, float],
) -> None:
    """Print a concise summary table to stdout."""
    all_results = import_results + read_results + aggregation_results
    width_name = max(
        (
            len(
                r.name
                if isinstance(r, BenchmarkResult)
                else r.split(" SKIPPED:")[0]
            )
            for r in all_results
        ),
        default=20,
    )

    header = (
        f"{'Benchmark':<{width_name}}  {'Mean (s)':>10}  {'Memory (MB)':>12}"
    )
    if has_previous:
        header += f"  {'Delta':>8}"
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))

    for section, section_results in [
        ("Import", import_results),
        ("Read", read_results),
        ("Aggregation", aggregation_results),
    ]:
        print(f"\n-- {section} --")
        for entry in section_results:
            if isinstance(entry, str):
                parts = entry.split(" SKIPPED:", 1)
                name = parts[0].strip()
                reason = parts[1].strip() if len(parts) > 1 else ""
                print(
                    f"  {name:<{width_name - 2}}  {'SKIPPED':>10}  {'':>12}  {reason[:40]}"
                )
            else:
                mean = entry.mean()
                memory = _format_memory(entry.peak_memory_mb)
                line = f"  {entry.name:<{width_name - 2}}  {mean:>10.4f}  {memory:>12}"
                if has_previous:
                    prev = previous_means.get(entry.name)
                    delta = _delta_str(mean, prev)
                    line += f"  {delta:>8}"
                print(line)

    print("=" * len(header) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the inewave benchmark suite and write benchmark_results.md."
    )
    parser.add_argument(
        "--iterations",
        "-n",
        type=int,
        default=10,
        metavar="N",
        help="Number of iterations per benchmark (default: 10).",
    )
    args = parser.parse_args()
    iterations: int = args.iterations

    if iterations < 1:
        parser.error("--iterations must be >= 1")

    previous_means: dict[str, float] = {}
    has_previous = False
    if _REPORT_PATH.exists():
        try:
            previous_text = _REPORT_PATH.read_text(encoding="utf-8")
            previous_means = _parse_previous_means(previous_text)
            if previous_means:
                has_previous = True
                print(
                    f"Previous results loaded from {_REPORT_PATH} "
                    f"({len(previous_means)} entries)."
                )
            else:
                print(
                    f"Warning: previous results file found at {_REPORT_PATH} "
                    "but could not parse any mean times. Delta column skipped."
                )
        except Exception as exc:
            print(
                f"Warning: failed to read previous results from {_REPORT_PATH}: {exc}. "
                "Delta column skipped."
            )

    print(f"\nRunning import benchmarks ({iterations} iterations each)...")
    import_results = run_all_import_benchmarks(iterations)
    for r in import_results:
        if isinstance(r, BenchmarkResult):
            print(f"  {r.name}: mean={r.mean():.4f}s")
        else:
            print(f"  {r}")

    print(f"\nRunning read benchmarks ({iterations} iterations each)...")
    read_results = run_all_read_benchmarks(iterations)
    for r in read_results:
        if isinstance(r, BenchmarkResult):
            print(f"  {r.name}: mean={r.mean():.4f}s")
        else:
            print(f"  {r}")

    print(f"\nRunning aggregation benchmarks ({iterations} iterations each)...")
    hidr_result = run_hidr_benchmark(iterations)
    nwlistop_aggregation_results = run_all_aggregation_benchmarks(iterations)
    aggregation_results: list[BenchmarkResult | str] = [
        hidr_result
    ] + nwlistop_aggregation_results
    for r in aggregation_results:
        if isinstance(r, BenchmarkResult):
            print(f"  {r.name}: mean={r.mean():.4f}s")
        else:
            print(f"  {r}")

    report = generate_report(
        import_results=import_results,
        read_results=read_results,
        aggregation_results=aggregation_results,
        iterations=iterations,
        previous_means=previous_means,
        has_previous=has_previous,
    )

    _REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {_REPORT_PATH}")

    _print_summary(
        import_results=import_results,
        read_results=read_results,
        aggregation_results=aggregation_results,
        has_previous=has_previous,
        previous_means=previous_means,
    )


if __name__ == "__main__":
    main()
