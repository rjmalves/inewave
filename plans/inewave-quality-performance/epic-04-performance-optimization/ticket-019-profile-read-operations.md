# ticket-019 Profile inewave read operations and identify bottlenecks

## Context

### Background

Epics 01-03 completed the cfinterface 1.9.0 upgrade, TabularSection migration, and schema versioning. These changes replaced the legacy `ValoresSerie` / `ValoresSeriePatamar` block classes with `TabelaSerieAnual` / `TabelaSeriePatamarAnual` base classes that use `TabularParser` for line parsing. The performance profile of inewave read operations has changed as a result: parsing now goes through `TabularParser.parse_lines()` -> `Line.read()` -> `Field._textual_read()` per line, and DataFrame construction goes through `_build_dataframe()` -> `formata_df_meses_para_datas_nwlistop()`. Before optimizing (tickets 020-021), we need to measure where time is actually spent.

### Relation to Epic

This ticket is the prerequisite for all optimization work in Epic 04. It produces a profiling report that identifies which code paths are bottlenecks, quantifying time distribution across: file I/O, line parsing, DataFrame construction, and the `__monta_tabela()` concatenation loop. Tickets 020 and 021 will use this report to target their optimizations.

### Current State

- There is no `benchmarks/` directory in the repository.
- There are 13 archive base classes in `inewave/nwlistop/modelos/arquivos/`, each with an identical `__monta_tabela()` method that iterates over parsed blocks and calls `pd.concat()` in a loop.
- Mock test data exists in `tests/mocks/arquivos/` as Python lists of strings (e.g., `MockEarmf` in `tests/mocks/arquivos/earmf.py` is ~2014 lines representing a multi-year file with ~2000 series).
- The parsing path is: `BlockFile.read()` -> `Block.read()` (one per year block) -> `TabularParser.parse_lines()` -> `Line.read()` -> `FloatField._textual_read()` (per field per line) -> `_build_dataframe()` -> `formata_df_meses_para_datas_nwlistop()`.
- The aggregation path is: `ArquivoXxx.valores` (lazy property) -> `__monta_tabela()` -> `pd.concat()` in a loop.
- `import inewave` eagerly imports all 3 subpackages (`newave`, `nwlistcf`, `nwlistop`), where `nwlistop/__init__.py` has 171 eager imports covering all handler classes.
- Test count baseline: 1134 tests.
- Python version: 3.10+. Dependencies: pandas >= 2.2.3, numpy >= 2.2.1, cfinterface >= 1.9.0.

## Specification

### Requirements

1. Create a `benchmarks/` directory at repository root with a profiling script `benchmarks/profile_read.py`.
2. The script must profile read operations for at least 6 representative files spanning all file-type families:
   - **Non-patamar REE**: `Earmf` (uses `ArquivoREE` + `TabelaSerieAnual`)
   - **Non-patamar SIN**: `Earmfsin` (uses `ArquivoSIN` + `TabelaSerieAnual`)
   - **Non-patamar Submercado**: `Cdef` (uses `ArquivoSubmercado` + `TabelaSerieAnual`)
   - **Patamar Submercado**: `Cmarg` (uses `ArquivoSubmercadoPatamar` + `TabelaSeriePatamarAnual`)
   - **Patamar REE**: `Earmfp` (uses `ArquivoREEPatamar` + `TabelaSeriePatamarAnual`)
   - **Newave SectionFile**: `Pmo` (large file, different parsing path)
3. For each file, the profiling must measure and report time breakdown into these categories:
   - **Total read time**: wall clock from `Handler.read(path)` call start to return
   - **Parsing time**: time inside `TabularParser.parse_lines()` (or equivalent Line.read calls)
   - **DataFrame construction time**: time in `_build_dataframe()` and `formata_df_meses_para_datas_nwlistop()`
   - **Aggregation time**: time in `__monta_tabela()` (the `pd.concat` loop)
   - **Import time**: time for `import inewave`
4. Use `cProfile` with `pstats` for function-level profiling and `time.perf_counter()` for wall-clock timing.
5. Produce output as a markdown report (`benchmarks/profile_report.md`) with tables and key findings.
6. Use mock data from `tests/mocks/arquivos/` for reproducibility (no dependency on external NEWAVE files).

### Inputs/Props

- Mock data files: `tests/mocks/arquivos/earmf.py` (`MockEarmf`), `tests/mocks/arquivos/cmarg.py` (`MockCmarg`), `tests/mocks/arquivos/earmfp.py` (`MockEarmfp`), `tests/mocks/arquivos/earmfsin.py` (`MockEarmfsin`), `tests/mocks/arquivos/cdef.py` (`MockCdef`).
- For `Pmo`, use the existing newave test infrastructure (check `tests/newave/test_pmo.py` for mock data source).

### Outputs/Behavior

- `benchmarks/profile_read.py`: Runnable script (`python benchmarks/profile_read.py`) that produces profiling output to stdout and writes `benchmarks/profile_report.md`.
- `benchmarks/profile_report.md`: Markdown file with:
  - Summary table: file type, total read time, parsing %, DataFrame %, aggregation %, other %
  - Per-file cProfile top-20 cumulative-time function list
  - Import time measurement for `import inewave`, `import inewave.nwlistop`, `import inewave.newave`
  - Key findings section identifying the top 3 bottlenecks
  - Recommendations section mapping each bottleneck to the ticket that addresses it (020, 021, or future)

### Error Handling

- If a mock data file is not found, skip that benchmark and print a warning rather than crashing.
- If cProfile output is empty for a handler, report "no data" rather than failing.

## Acceptance Criteria

- [ ] Given the repository has no `benchmarks/` directory, when the ticket is complete, then `benchmarks/profile_read.py` and `benchmarks/__init__.py` exist
- [ ] Given `benchmarks/profile_read.py` exists, when running `python benchmarks/profile_read.py` from the repo root, then the script completes without errors and produces `benchmarks/profile_report.md`
- [ ] Given the script has run, when reading `benchmarks/profile_report.md`, then it contains a summary table with at least 5 file types and columns: File Type, Total Time (s), Parsing %, DataFrame %, Aggregation %, Other %
- [ ] Given the script has run, when reading the report, then import time measurements for `inewave`, `inewave.nwlistop`, and `inewave.newave` are present
- [ ] Given the script has run, when reading the report, then a "Key Findings" section identifies at least 2 specific bottleneck functions with their cumulative time percentages
- [ ] Given the profiling script exists, when running `pytest tests/ -x -q`, then all 1134 existing tests still pass (no regressions)

## Implementation Guide

### Suggested Approach

1. Create `benchmarks/__init__.py` (empty) and `benchmarks/profile_read.py`.
2. In `profile_read.py`:
   a. Write a helper function that profiles a single handler read operation using `cProfile.Profile()` context manager.
   b. For each nwlistop handler, use the `mock_open` + `patch("builtins.open", m)` pattern from existing tests (see `tests/nwlistop/test_earmf.py` lines 12-13 for the pattern: `m = mock_open(read_data="".join(MockEarmf)); with patch("builtins.open", m): n = Earmf.read(ARQ_TESTE)`).
   c. For import timing, use `importlib.reload()` after clearing relevant `sys.modules` entries, wrapped in `time.perf_counter()`.
   d. Extract stats using `pstats.Stats` and filter for key functions: `parse_lines`, `_build_dataframe`, `formata_df_meses_para_datas`, `__monta_tabela`, `_textual_read`, `concat`.
   e. Generate the markdown report programmatically.
3. Run the script once and commit the report alongside the script.

### Key Files to Modify

- **Create**: `benchmarks/__init__.py` (empty file)
- **Create**: `benchmarks/profile_read.py` (profiling script, ~200-300 LOC)
- **Create**: `benchmarks/profile_report.md` (generated output, committed for baseline reference)

### Patterns to Follow

- Use the same mock-open test pattern from `tests/nwlistop/test_earmf.py`:
  ```python
  from tests.mocks.mock_open import mock_open
  from unittest.mock import patch
  m = mock_open(read_data="".join(MockData))
  with patch("builtins.open", m):
      handler = Handler.read(path)
  ```
- Use `cProfile.Profile()` as a context manager for targeted profiling:
  ```python
  import cProfile, pstats, io
  pr = cProfile.Profile()
  pr.enable()
  # ... code to profile ...
  pr.disable()
  s = io.StringIO()
  ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
  ps.print_stats(20)
  ```

### Pitfalls to Avoid

- Do NOT use `py-spy` or any tool requiring root access; stick to `cProfile` which is stdlib.
- Do NOT add profiling dependencies to `pyproject.toml`; `cProfile` and `pstats` are stdlib.
- Do NOT modify any source files in `inewave/`; this ticket only creates files in `benchmarks/`.
- Mock data files like `tests/mocks/arquivos/earmf.py` can be very large (~260KB). Import them as modules, do not try to read them as text files.
- The `mock_open` helper is at `tests/mocks/mock_open.py`, not unittest.mock's built-in. Use the project's version.
- When measuring `__monta_tabela`, note it is a private method accessed via the `valores` lazy property. Profile by accessing `handler.valores` after `handler.read()`.

## Testing Requirements

### Unit Tests

No new unit tests required. This ticket produces a profiling script, not library code.

### Integration Tests

- Verify the profiling script runs end-to-end: `python benchmarks/profile_read.py` exits with code 0.
- Verify `benchmarks/profile_report.md` is generated and non-empty.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-013 (deprecated block cleanup must be complete; already done)
- **Blocks**: ticket-020, ticket-021

## Effort Estimate

**Points**: 2
**Confidence**: High
