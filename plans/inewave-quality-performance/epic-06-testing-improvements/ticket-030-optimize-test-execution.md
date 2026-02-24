# ticket-030 Optimize test execution (parallel, fixtures, mock improvements)

## Context

### Background

The inewave test suite currently has 1134 tests that run in 41.32 seconds on a modern Linux machine (Fedora 43, kernel 6.18). After tickets 027-029 are completed, the suite will grow to approximately 1310+ tests (adding ~160 nwlistop round-trip tests, ~17 newave round-trip tests, and 4 validation tests). This growth makes it increasingly important to keep the test suite fast for developer iteration.

The current test infrastructure has several characteristics worth examining:

- **No `conftest.py` files** exist anywhere in the `tests/` directory tree.
- **No pytest-xdist** for parallel execution (only `pytest` and `pytest-cov` are in dev dependencies).
- **Every test function creates its own `mock_open`** instance, even when many tests in the same file use identical mock data.
- **No session-scoped or module-scoped fixtures** for shared mock data.
- **No pytest configuration** in `pyproject.toml` (no `[tool.pytest.ini_options]` section).
- Test collection is fast (0.45s for 1134 tests), confirming the lazy import optimization from ticket-021 is working.

### Relation to Epic

This ticket targets the fourth goal of Epic 06: "Improve test performance (parallel execution, reduced mock overhead)." It is the infrastructure improvement ticket for the testing epic, focused on reducing wall-clock time for the full test suite.

### Current State

**Test suite timing breakdown** (estimated from `pytest tests/ --durations=0`):

- `tests/newave/` contains 64 test files with 499 test functions. The newave tests take the bulk of the time because several files use real binary data files (`hidr.dat`, `energiab.dat`, `forward.dat`, etc.) rather than lightweight mocks.
- `tests/nwlistop/` contains 172 test files with 565 test functions. The nwlistop tests are individually fast (mock_open based) but numerous.
- `tests/nwlistcf/` contains 7 test files with a small number of tests.

**Current dependencies** in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-cov",
    "ruff",
    "mypy",
]
```

**Test isolation analysis**:

- Each test function creates its own `mock_open` instance -- tests are fully isolated.
- Binary file tests (`hidr`, `energiab`, `forward`, etc.) read from files on disk but do not modify them -- safe for parallel execution.
- MEDIAS CSV tests read from `tests/_arquivos/` on disk but do not modify them -- safe for parallel execution.
- No shared mutable state (no module-level variables that get modified, no database connections).
- The custom `mock_open` in `tests/mocks/mock_open.py` uses a module-level `file_spec` variable that is populated lazily. This is read-only after first access and safe for multi-process parallelism.

## Specification

### Requirements

1. **Add pytest-xdist** to dev dependencies for parallel test execution.
2. **Add `[tool.pytest.ini_options]`** to `pyproject.toml` with sensible defaults.
3. **Create `tests/conftest.py`** with session-scoped fixtures for the most commonly used mock data patterns.
4. **Verify parallel execution** works correctly with `pytest -n auto`.
5. **Measure and document** the performance improvement.

### Inputs/Props

- `pyproject.toml` -- add pytest-xdist dependency and pytest configuration.
- `tests/conftest.py` -- new file with shared fixtures.

### Outputs/Behavior

- `pytest tests/ -n auto` runs the full suite in parallel using all available CPU cores.
- Wall-clock time for the full suite decreases significantly (target: < 20 seconds with 4+ cores).
- All tests still pass when run sequentially (`pytest tests/`) and in parallel (`pytest tests/ -n auto`).

### Error Handling

- If any test fails under parallel execution but passes sequentially, it indicates a test isolation issue that must be investigated (not suppressed).
- If pytest-xdist introduces import issues with the lazy import `__init__.py` modules, they must be fixed in the test setup, not by reverting the lazy imports.

## Acceptance Criteria

- [ ] Given `pyproject.toml` is updated, when `uv sync --extra dev` (or equivalent) is run, then `pytest-xdist` is installed in the dev environment
- [ ] Given the pytest configuration is added to `pyproject.toml`, when `pytest tests/` is run without flags, then it uses the configured defaults (testpaths, warning filters for DeprecationWarning)
- [ ] Given `tests/conftest.py` is created, when `pytest tests/ --co` is run, then fixtures are discoverable and no collection errors occur
- [ ] Given pytest-xdist is installed, when `pytest tests/ -n auto` is run, then all tests pass with zero failures
- [ ] Given the full test suite (post-tickets 027-029), when `pytest tests/ -n auto` is run on a machine with 4+ cores, then wall-clock time is less than 25 seconds (target improvement: at least 40% faster than sequential)
- [ ] Given the full test suite, when `pytest tests/` is run without `-n` (sequential), then all tests still pass (no regression from infrastructure changes)

## Implementation Guide

### Suggested Approach

1. **Add pytest-xdist to dev dependencies** in `pyproject.toml`:

   ```toml
   [project.optional-dependencies]
   dev = [
       "pytest",
       "pytest-cov",
       "pytest-xdist",
       "ruff",
       "mypy",
   ]
   ```

2. **Add pytest configuration** to `pyproject.toml`:

   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   filterwarnings = [
       "ignore::DeprecationWarning:inewave.nwlistop",
   ]
   ```

   This suppresses the known `DeprecationWarning` from deprecated nwlistop handler `__init__` methods (e.g., `Vturuh`), which currently generate 108 warnings.

3. **Create `tests/conftest.py`** with shared fixtures. Focus on the most impactful optimizations:

   ```python
   """Shared test fixtures for inewave test suite."""

   import pytest


   @pytest.fixture(scope="session")
   def hidr_data():
       """Session-scoped fixture for hidr.dat binary data."""
       with open("./tests/mocks/arquivos/hidr.dat", "rb") as f:
           return f.read()
   ```

   However, be careful: most newave tests with real binary files already use `Hidr.read(ARQ_TESTE)` directly (not fixtures). Introducing fixtures would require modifying existing test files, which is out of scope for this ticket. The conftest.py should instead focus on:

   a. **Warning filters** (if not handled by pyproject.toml alone)
   b. **Session-scoped marker registration** for any custom markers
   c. **A `tmp_path` factory** for round-trip tests that may benefit from writing to actual temp files instead of mock_open (future optimization)

   The primary value of conftest.py in this ticket is as a foundation for future test improvements, not as a performance optimization itself. The main performance win comes from pytest-xdist parallelism.

4. **Verify parallel execution**:

   ```bash
   # Sequential baseline
   pytest tests/ -q --tb=no 2>&1 | tail -3

   # Parallel execution
   pytest tests/ -n auto -q --tb=no 2>&1 | tail -3
   ```

5. **Document the results** in the test run output. If any tests fail under parallel execution, investigate and fix the isolation issue.

6. **Optional: Add a Makefile/script shortcut** for common test invocations:
   - `pytest tests/` -- sequential
   - `pytest tests/ -n auto` -- parallel
   - `pytest tests/ -n auto --cov=inewave` -- parallel with coverage

### Key Files to Modify

- `pyproject.toml` -- add `pytest-xdist` to `[project.optional-dependencies] dev` and add `[tool.pytest.ini_options]` section
- `tests/conftest.py` -- new file (currently does not exist)

### Patterns to Follow

- Follow the convention from epic-05 learnings: dependencies use `>=` floor, not `==` pin.
- The `filterwarnings` in pytest configuration follows the same pattern used by cfinterface: `"ignore::DeprecationWarning:module_path"`.
- No DeprecationWarning suppression in production code (warnings must be eliminated at the source) -- this is test-only configuration.

### Pitfalls to Avoid

- **Do NOT modify existing test files** in this ticket -- only infrastructure changes (pyproject.toml, conftest.py).
- **Do NOT use `pytest-xdist` `--forked` mode** -- it is unnecessary and adds overhead. Use `-n auto` which uses `multiprocessing`.
- **Do NOT set `-n auto` as the default** in `[tool.pytest.ini_options]` -- developers should opt into parallel execution explicitly. Running sequential by default is safer for debugging.
- **The `file_spec` global in `tests/mocks/mock_open.py`** is lazily initialized on first call to `mock_open()`. Under pytest-xdist, each worker process gets its own copy, so this is safe. Do NOT try to make it thread-safe.
- **Do NOT add `conftest.py` files in subdirectories** (tests/newave/conftest.py, tests/nwlistop/conftest.py) -- keep it simple with one root conftest.py.
- **pytest-xdist worker scheduling**: The default `loadfile` scheduler groups tests from the same file to the same worker, which is optimal for this codebase (tests in the same file share mock data imports). Do NOT change the scheduler.

## Testing Requirements

### Unit Tests

Not applicable -- this ticket modifies test infrastructure, not production code or test logic.

### Integration Tests

The full test suite (`pytest tests/ -n auto`) is the integration test for this ticket.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-027, ticket-028, ticket-029 (this ticket should run after all round-trip tests are added, so the parallel execution test covers the full expanded suite)
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High
