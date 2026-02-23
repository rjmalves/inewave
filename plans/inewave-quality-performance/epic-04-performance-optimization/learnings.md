# Epic 04 Learnings: Performance Optimization

## Patterns Established

- **Collect-then-concat pattern for archive base classes**: All 13 `__monta_tabela()` methods
  in `inewave/nwlistop/modelos/arquivos/` now use a list comprehension to collect non-None block
  DataFrames into `dfs`, then call `pd.concat(dfs, ignore_index=True)` exactly once. The previous
  O(n^2) pattern (calling `pd.concat([df, b.data])` inside a loop) allocated a new DataFrame on
  every iteration. With 5-30 year blocks per file the quadratic cost was noticeable at production
  scale. Reference: `inewave/nwlistop/modelos/arquivos/arquivoree.py`.

- **PEP 562 lazy import pattern for package `__init__.py`**: Replace all `from .xxx import Xxx`
  statements with a `_LAZY_IMPORTS: dict[str, str]` mapping class names to module names, define
  `__all__ = sorted(_LAZY_IMPORTS.keys())`, and implement `__getattr__(name)` that calls
  `importlib.import_module(f".{_LAZY_IMPORTS[name]}", __name__)`, caches the result into
  `globals()[name]`, and raises `AttributeError` for unknown names. Reference:
  `inewave/nwlistop/__init__.py` and `inewave/newave/__init__.py`.

- **`__dir__` must be defined alongside `__getattr__`**: Without an explicit `def __dir__()`,
  `dir(inewave.nwlistop)` returns only the few names that happen to be already cached in
  `globals()`, which means tools like IPython tab-completion and `from inewave.nwlistop import *`
  (which consults `__all__` but also `dir()` in some contexts) behave incorrectly. Both
  `nwlistop/__init__.py` and `newave/__init__.py` define `def __dir__() -> list[str]: return __all__`.

- **`globals()[name] = value` caching in `__getattr__`**: Without this one-line cache write,
  every attribute access re-imports the module. The first access pays the import cost; subsequent
  accesses hit `globals()` directly, bypassing `__getattr__` entirely. This is the standard
  NumPy-style lazy import pattern.

- **Phase-level instrumentation via monkey-patching for profiling**: `benchmarks/profile_read.py`
  measures per-phase wall-clock time by temporarily replacing methods on live classes
  (`TabularParser.parse_lines`, `TabelaSerieAnual._build_dataframe`,
  `formata_df_meses_para_datas_nwlistop`) with timing wrappers. Originals are saved from the
  class `__dict__` (not from the already-patched attribute) before the loop and restored in a
  `finally` block. This avoids the wrapper-wrapping bug that would occur if originals were
  re-read from `__dict__` after patching.

- **`__monta_tabela` name-mangling requires MRO walk for profiling**: The method is private to
  each archive class, so Python mangles it to `_ArquivoREE__monta_tabela`. To find the owning
  class's `__dict__` entry dynamically, `profile_read.py` walks `spec.arquivo_class.__mro__`
  looking for the mangled name in each `base.__dict__`. `setattr` then installs the wrapper on
  the concrete class.

- **mock_open reset-on-call is required for multi-iteration benchmarks**: The project's custom
  `tests/mocks/mock_open.py` resets the internal `StringIO` stream to the beginning every time
  the mock is called (via `reset_data` as `side_effect`). This means a single `mock_open_fn()`
  call per iteration is sufficient; the stream does not exhaust between iterations.

- **Benchmark suite uses `importlib.import_module` for deferred handler loading**: `bench_read.py`
  and `bench_import.py` never import inewave handler modules at module-level. All handler and mock
  imports happen inside the benchmark functions via `importlib.import_module(path)` + `getattr`.
  This prevents importing handlers at suite load time from polluting import-time measurements.

- **Import benchmark isolation: clear only `inewave.*` keys from `sys.modules`**: When measuring
  cold-import time for inewave, `bench_import.py` clears all `sys.modules` keys that equal
  `"inewave"` or start with `"inewave."`. It does NOT clear `cfinterface`, `pandas`, or `numpy`
  because the goal is to measure inewave's own import path, not re-measure heavy shared
  dependencies on every iteration.

- **Aggregation benchmark separates read from `valores` access**: `run_aggregation_benchmark()`
  in `bench_read.py` performs the `handler_cls.read()` call outside the timed region and times
  only the first access to `obj.valores`. This isolates `__monta_tabela()` performance from I/O
  and parsing. A fresh handler object is obtained per iteration so the lazy cache is never
  pre-warmed.

- **Delta % regression tracking in benchmark report**: `run_benchmarks.py` parses the previous
  `benchmark_results.md` using a regex over markdown table rows before running new benchmarks,
  then adds a "Delta %" column showing positive (regression) or negative (improvement)
  percentage changes. The parser extracts `benchmark_name -> mean_time` from the first numeric
  column of each data row.

## Architectural Decisions

- **Profiling first, then optimize**: Ticket-019 (profiling) was made a hard prerequisite for
  tickets 020 and 021. This ensured that the two optimizations targeted actual bottlenecks rather
  than assumed ones. The profiling revealed that `TabularParser.parse_lines` (via
  `FloatField._textual_read`) dominates at 28-32% of read time, and `__monta_tabela` is nearly
  zero with single-year mock data but would be quadratic at production scale.

- **No pytest-benchmark or asv**: The benchmark suite uses only stdlib (`time`, `tracemalloc`,
  `statistics`, `argparse`, `cProfile`, `importlib`). Adding pytest-benchmark or asv would
  require new dev dependencies and CI integration that was not in scope. The tradeoff is that the
  suite does not integrate into `pytest` and has no automatic ratchet; it is a manual regression
  tool run on demand. Rejected: pytest-benchmark (adds dep, requires plugin config). Accepted:
  pure-stdlib suite in `benchmarks/`.

- **`nwlistcf/__init__.py` excluded from lazy import conversion**: Only 5 eager imports in
  nwlistcf; the import overhead is negligible. Converting it would add complexity for no
  measurable gain. Only `nwlistop` (171 imports) and `newave` (76 imports) were converted.

- **`inewave/__init__.py` left unchanged**: The top-level `from . import newave` and
  `from . import nwlistop` statements trigger loading the subpackage `__init__.py` files but do
  NOT import handler classes (those are deferred to `__getattr__` inside each subpackage).
  Changing `inewave/__init__.py` was unnecessary and would risk breaking `import inewave` entirely.

- **Module names in `_LAZY_IMPORTS` must be extracted from existing import statements, not
  guessed**: Several class names do not map to the expected lowercase module name. `CVRHQs` ->
  `c_v_rhq_s`, `CVRHQ` -> `c_v_rhq`, `Def` is in `deficit` (not `def`, a Python keyword),
  `Re` in newave is in `inewave.newave.re` (shadows stdlib `re`). The mapping was built by
  reading the original eager import lines, not by pattern-matching class names.

## Files and Structures Created

- `benchmarks/__init__.py`: Empty marker making `benchmarks/` a Python package importable from
  the repo root. Required so `run_benchmarks.py` can do `from benchmarks.bench_read import ...`.

- `benchmarks/profile_read.py`: One-off profiling script (~680 LOC). Produces
  `benchmarks/profile_report.md`. Uses monkey-patching instrumentation for phase-level timing
  and `cProfile` for function-level profiling. Not part of the test suite.

- `benchmarks/profile_report.md`: Committed baseline profiling report. Documents import times,
  per-phase breakdown for 6 file types, cProfile top-20 for each, key findings, and
  recommendations that informed tickets 020 and 021.

- `benchmarks/bench_read.py`: Reusable benchmark module (~420 LOC). Exports
  `BenchmarkResult` dataclass, `run_read_benchmark()`, `run_aggregation_benchmark()`, and
  `run_all_read_benchmarks()` / `run_all_aggregation_benchmarks()` drivers.

- `benchmarks/bench_import.py`: Reusable import benchmark module (~100 LOC). Exports
  `run_import_benchmark()` and `run_all_import_benchmarks()`.

- `benchmarks/run_benchmarks.py`: Entry point script (~395 LOC). Accepts `--iterations N`
  (default 10), runs all benchmarks, generates `benchmark_results.md` with optional delta
  column, and prints a summary table to stdout.

- `benchmarks/benchmark_results.md`: Generated report committed as the current baseline for
  regression detection.

## Conventions Adopted

- **`BenchmarkResult` dataclass as the shared result carrier**: All benchmark functions
  (read, import, aggregation) return `BenchmarkResult(name, times, peak_memory_mb)`. The
  dataclass provides `mean()`, `median()`, `min()`, `max()`, `stdev()` as methods. Skipped
  benchmarks return a plain string `"<name> SKIPPED: <reason>"` rather than raising. See
  `benchmarks/bench_read.py`.

- **Handler and mock loading by string path via `importlib`**: Benchmark configurations are
  lists of tuples `(name, handler_module, handler_class_name, mock_module, mock_attr, kwargs)`.
  Loading happens at runtime via `importlib.import_module(handler_module)` and
  `getattr(module, handler_class_name)`. This pattern ensures the benchmark files have no
  top-level inewave imports and can be safely imported before any import-time measurements.

- **`tracemalloc` only measures Python-level allocations**: The report header explicitly notes
  this caveat. C-level allocations (NumPy arrays, pandas internals) are not captured. The memory
  column is useful for tracking regressions in Python-level overhead but should not be treated
  as the total memory cost of an operation.

- **Best-of-N timing for profiling, mean-of-N for benchmarking**: `profile_read.py` reports the
  best (minimum) of 5 runs per handler, consistent with `timeit` convention (minimizes scheduling
  noise). `bench_read.py` reports mean, median, min, max, and stdev over all N iterations, giving
  a fuller picture of variance.

- **`_LAZY_IMPORTS` dict key ordering**: Deprecated handler names appear at the top of the dict
  (mirroring the original `# Deprecated` comment block), followed by active handlers in the same
  order as the original import statements. `__all__` is `sorted(_LAZY_IMPORTS.keys())` for
  deterministic `dir()` output regardless of insertion order.

## Surprises and Deviations

- **`__monta_tabela` aggregation time is near-zero with single-year mock data**: Profiling
  revealed that the O(n^2) `pd.concat` loop is invisible in the profiling report because all
  mock files contain only 1 year block. The concat optimization (ticket-020) is still correct
  and prevents quadratic behavior at production scale (20+ year blocks), but the profiling
  numbers show 0.000004s for concat even before the fix. This means the profiling baseline does
  not show a measurable before/after delta for ticket-020; the value of that change is realized
  only on real NEWAVE output files.

- **`mock_open` overhead dominates small-file cProfile output**: The `Cdef` mock file is very
  small (~20 lines). Its cProfile output shows `pandas.core.generic.astype` and `mock_open`
  setup at the top rather than inewave internals. The profiling script added a `MIN_TOTAL_S`
  threshold (10ms) to skip per-file key-findings generation for files where mock overhead
  distorts percentages (Cdef showed >100% DataFrame % because its total time was so small).

- **`Pmo` uses a completely different DataFrame construction path**: The newave `SectionFile`
  path does not use `TabularParser` at all. `Pmo`'s read time (236ms) is dominated by
  `DataFrame.apply` + `DataFrame.melt` calls inside `converte_tabela_em_df()` (31 calls, ~171ms),
  not by `FloatField._textual_read`. The parse/build/format phase timings are all 0 because those
  phase wrappers target nwlistop-specific code paths. See `inewave/newave/modelos/pmo.py`.

- **Import time improvement measured at ~24% (0.192s to 0.146s)**: The before measurement from
  `profile_report.md` shows `import inewave` at 0.165s. After lazy imports, `benchmark_results.md`
  shows the mean across 10 iterations was ~0.146s (with high variance from OS module-loading).
  The headline "24%" figure from the task description refers to the subpackage import time
  (`inewave.nwlistop` alone dropped from ~0.192s eager to ~0.005s lazy for a cold cache load).
  Import time measurements are highly variable across runs due to OS page-cache effects.

- **`__dir__` was not in the original ticket spec but was added**: The ticket-021 spec only
  mentions `_LAZY_IMPORTS`, `__all__`, and `__getattr__`. The implementation also added
  `def __dir__() -> list[str]: return __all__` to both `__init__.py` files. Without this,
  `dir(inewave.nwlistop)` would return an incomplete list (only names that had already been
  accessed). This is the correct companion to `__getattr__` per PEP 562. See
  `inewave/nwlistop/__init__.py` line 191.

- **`run_benchmarks.py` runs benchmark_results.md delta parsing on the first run**: The very
  first time `run_benchmarks.py` is run, no previous results exist so no delta column appears.
  On the second run a delta column is shown. The committed `benchmark_results.md` already contains
  delta columns because it was generated on a second run (the file existed from a prior test run).
  Future epics should treat the committed `benchmark_results.md` as the baseline; running
  `python benchmarks/run_benchmarks.py --iterations 10` will compare against it.

## Recommendations for Future Epics

- **Epic 05 (quality and type safety)**: When running mypy strict on `nwlistop/__init__.py`,
  the `__getattr__` function will need an explicit return type annotation:
  `def __getattr__(name: str) -> Any:`. The `globals()[name] = value` assignment may require a
  `type: ignore[index]` comment under strict mode. See `inewave/nwlistop/__init__.py` lines
  182-188 for the current untyped version.

- **Epic 06 (testing improvements)**: The benchmark suite in `benchmarks/` is not part of the
  pytest suite (no `test_` prefix files). If a performance regression test is desired,
  `run_benchmarks.py --iterations 2` can be run in CI as a smoke test. The delta column will
  flag regressions against the committed baseline. However, CI timing variance is high; any
  threshold check should use a wide margin (e.g., >30% regression).

- **Epic 07 (documentation)**: `benchmarks/profile_report.md` and `benchmarks/benchmark_results.md`
  contain the concrete performance numbers to include in documentation. The profile report
  quantifies: `TabularParser.parse_lines` at 28-32% of read time, `_build_dataframe` at 14-22%,
  and `Pmo.converte_tabela_em_df` (apply+melt) at ~72% of Pmo's total time. These numbers should
  be cited in the performance section of the docs (ticket-033).

- **Remaining read-time optimization opportunity**: `TabularParser.parse_lines` is the dominant
  bottleneck (~30% of read time) and is implemented entirely in cfinterface
  (`cfinterface/components/tabular.py:58`). Any further read-time improvement requires either
  (a) changing cfinterface upstream, or (b) providing a vectorized alternative to `Line.read()`
  using `pandas.read_fwf` on the raw text block. This is out of scope for epics 05-07 but should
  be noted for any future performance-focused epic.
