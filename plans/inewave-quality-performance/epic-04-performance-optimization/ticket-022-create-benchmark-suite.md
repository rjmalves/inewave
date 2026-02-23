# ticket-022 Create benchmark suite for read performance

## Context

### Background

Tickets 019-021 introduced profiling, DataFrame optimization, and lazy imports. To prevent performance regressions and provide concrete numbers for documentation (Epic 07), inewave needs a reproducible benchmark suite that can be run on demand to measure read performance across representative file types. Unlike the one-off profiling script from ticket-019, this benchmark suite is designed for repeated use: before/after comparisons, CI integration, and ongoing tracking.

### Relation to Epic

This is the capstone ticket of Epic 04. It takes the optimizations from tickets 020-021, the profiling infrastructure from ticket-019, and wraps them into a reusable benchmark suite. The results feed into Epic 07's documentation work (ticket-033 specifically mentions adding performance benchmarks to docs).

### Current State

- `benchmarks/profile_read.py` exists from ticket-019, providing one-off cProfile-based profiling.
- `benchmarks/profile_report.md` exists with baseline profiling results.
- The 13 archive base classes have been optimized (ticket-020) with collect-then-concat.
- Lazy imports are in place (ticket-021) for nwlistop and newave.
- Mock test data exists in `tests/mocks/arquivos/` as Python lists of strings.
- `pyproject.toml` has `[project.optional-dependencies] dev = [...]` for dev dependencies.
- No pytest-benchmark or asv is currently installed.
- Test count baseline: 1134 tests.

## Specification

### Requirements

1. Create `benchmarks/bench_read.py` with benchmark functions for representative file types using `time.perf_counter()` for wall-clock timing and `tracemalloc` for peak memory measurement.
2. Benchmark the following operations:
   - **Import time**: `import inewave` (with `sys.modules` cleanup between runs)
   - **Import time**: `from inewave.nwlistop import Earmf` (single handler import)
   - **Read non-patamar REE**: `Earmf.read()` with `MockEarmf` data
   - **Read non-patamar SIN**: `Earmfsin.read()` with `MockEarmfsin` data
   - **Read patamar Submercado**: `Cmarg.read()` with `MockCmarg` data
   - **Read patamar REE**: `Earmfp.read()` with `MockEarmfp` data
   - **Read newave SectionFile**: `Pmo.read()` with mock data
   - **Read newave BinaryFile**: `Hidr.read()` with mock data
   - **Aggregation (valores property)**: For each nwlistop handler above, time the `handler.valores` access separately from the `read()` call
3. Each benchmark must:
   - Run a configurable number of iterations (default: 10) for statistical validity
   - Report: mean, median, min, max, std dev of wall-clock time
   - Report: peak memory delta (via `tracemalloc`)
4. Create `benchmarks/bench_import.py` for import-specific benchmarks (separated because import benchmarks require `sys.modules` manipulation).
5. Create `benchmarks/run_benchmarks.py` as the entry point that runs all benchmark suites and produces a consolidated markdown report at `benchmarks/benchmark_results.md`.
6. The report must include:
   - Timestamp and system info (Python version, platform, CPU)
   - Table per benchmark category (import, read, aggregation)
   - Mean time, std dev, peak memory for each benchmark
   - Comparison support: if a previous `benchmarks/benchmark_results.md` exists, load it and add a "Delta %" column showing improvement/regression

### Inputs/Props

- Mock data from `tests/mocks/arquivos/` (imported as Python modules).
- Number of iterations: configurable via command-line argument (default: 10).

### Outputs/Behavior

- `benchmarks/bench_read.py`: Module with benchmark functions for read operations.
- `benchmarks/bench_import.py`: Module with benchmark functions for import operations.
- `benchmarks/run_benchmarks.py`: Entry point script. Usage: `python benchmarks/run_benchmarks.py [--iterations N]`.
- `benchmarks/benchmark_results.md`: Generated markdown report with timing tables.
- Exit code 0 on success.

### Error Handling

- If a mock data module cannot be imported (e.g., the mock file was removed), skip that benchmark and report it as "SKIPPED" in the results table.
- If `tracemalloc` measurement fails, report memory as "N/A" rather than crashing.
- If the previous results file cannot be parsed for comparison, skip the delta column and print a warning.

## Acceptance Criteria

- [ ] Given the benchmark suite exists, when running `python benchmarks/run_benchmarks.py`, then it completes without errors and produces `benchmarks/benchmark_results.md`
- [ ] Given the script has run, when reading `benchmarks/benchmark_results.md`, then it contains tables for import benchmarks, read benchmarks, and aggregation benchmarks
- [ ] Given the report, when reading any benchmark row, then it shows mean, median, min, max, std dev (in seconds), and peak memory (in MB)
- [ ] Given the script is run with `--iterations 3`, when checking the report, then each benchmark ran exactly 3 iterations
- [ ] Given a previous `benchmark_results.md` exists, when running the benchmarks again, then the new report includes a "Delta %" column comparing new vs old mean times
- [ ] Given the benchmark suite exists, when running `pytest tests/ -x -q`, then all 1134 tests still pass (benchmark files do not interfere with test suite)
- [ ] Given the benchmark suite, when inspecting `benchmarks/`, then it contains: `__init__.py`, `bench_read.py`, `bench_import.py`, `run_benchmarks.py`, and `benchmark_results.md`

## Implementation Guide

### Suggested Approach

1. **Create `benchmarks/__init__.py`** (if not already created by ticket-019; ensure it exists).

2. **Create `benchmarks/bench_read.py`:**
   - Define a `BenchmarkResult` dataclass: `name`, `times` (list of floats), `peak_memory_mb` (float).
   - Write a `run_read_benchmark(handler_cls, mock_data, name, iterations)` function that:
     a. Joins mock data into a string: `"".join(mock_data)`
     b. For each iteration: creates `mock_open(read_data=...)`, patches `builtins.open`, calls `handler_cls.read(path)`, accesses `handler.valores`, times each phase separately.
     c. Returns `BenchmarkResult`.
   - Define benchmark configurations as a list of dicts: `{"name": "Earmf (REE, non-patamar)", "handler": "inewave.nwlistop.earmf.Earmf", "mock": "tests.mocks.arquivos.earmf.MockEarmf"}`.
   - Use `importlib.import_module` + `getattr` to load handlers and mocks by string path (avoids eagerly importing everything at benchmark module load time).

3. **Create `benchmarks/bench_import.py`:**
   - Write `run_import_benchmark(module_path, iterations)` that:
     a. For each iteration: clears `sys.modules` of `inewave.*` entries, measures `importlib.import_module(module_path)` time.
     b. Returns `BenchmarkResult`.
   - Benchmark: `inewave`, `inewave.nwlistop`, `inewave.newave`, `inewave.nwlistop.earmf` (single handler).

4. **Create `benchmarks/run_benchmarks.py`:**
   - Parse `--iterations` from `sys.argv` (use `argparse`).
   - Run all import benchmarks, then all read benchmarks.
   - Collect all `BenchmarkResult`s.
   - Generate markdown report with tables.
   - If previous results file exists, parse it and compute delta percentages.
   - Write to `benchmarks/benchmark_results.md`.
   - Print summary to stdout.

5. **Use `time.perf_counter()`** for timing (not `timeit`, which adds complexity with no benefit here since we control the iteration loop).

6. **Use `tracemalloc`** for memory:
   ```python
   tracemalloc.start()
   # ... benchmark code ...
   _, peak = tracemalloc.get_traced_memory()
   tracemalloc.stop()
   peak_mb = peak / (1024 * 1024)
   ```

### Key Files to Modify

- **Create**: `benchmarks/__init__.py` (if not exists; empty)
- **Create**: `benchmarks/bench_read.py` (~150 LOC)
- **Create**: `benchmarks/bench_import.py` (~80 LOC)
- **Create**: `benchmarks/run_benchmarks.py` (~200 LOC)
- **Create**: `benchmarks/benchmark_results.md` (generated on first run)

### Patterns to Follow

- Use the mock-open pattern from `tests/nwlistop/test_earmf.py` for read benchmarks:
  ```python
  from tests.mocks.mock_open import mock_open
  from unittest.mock import patch
  m = mock_open(read_data="".join(MockData))
  with patch("builtins.open", m):
      handler = Handler.read("dummy_path.out")
  ```
- Use `argparse` for CLI arguments (consistent with Python conventions).
- Use `statistics` module for mean, median, stdev.
- Report times in seconds with 4 decimal places; memory in MB with 2 decimal places.

### Pitfalls to Avoid

- Do NOT add `pytest-benchmark` or `asv` as dependencies. Use only stdlib (`time`, `tracemalloc`, `statistics`, `argparse`, `cProfile`).
- Do NOT import inewave handler modules at the top of benchmark files. Use `importlib.import_module` to load them on demand, so import benchmarks are not polluted.
- When clearing `sys.modules` for import benchmarks, only clear keys starting with `"inewave"`. Do NOT clear `cfinterface`, `pandas`, `numpy`, etc. (those represent library load time, not inewave load time).
- Do NOT run benchmarks as part of the `pytest` test suite. The `benchmarks/` directory should not contain `test_` prefixed files.
- The `tests/mocks/mock_open.py` helper must be importable from the benchmark scripts. Ensure `PYTHONPATH` includes the repo root or use `sys.path` manipulation.
- `tracemalloc` measures Python-level allocations only. Report this caveat in the benchmark results header.

## Testing Requirements

### Unit Tests

No new unit tests. The benchmark suite is a standalone tool, not library code.

### Integration Tests

- Verify `python benchmarks/run_benchmarks.py --iterations 2` runs without errors.
- Verify `benchmarks/benchmark_results.md` is generated and contains the expected table structure.
- Run `pytest tests/ -x -q` to verify no regression (benchmark files must not interfere).

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-020 (optimized DataFrame creation provides the baseline to benchmark)
- **Blocks**: None (but results inform ticket-033 in Epic 07)

## Effort Estimate

**Points**: 3
**Confidence**: Medium
