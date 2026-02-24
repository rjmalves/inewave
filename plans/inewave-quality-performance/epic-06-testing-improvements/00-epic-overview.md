# Epic 06: Testing Improvements

## Goals

1. Add round-trip tests (read -> write -> read) for all file types
2. Add version-aware tests exercising `read(version=...)` API
3. Add validation tests exercising `validate()` API
4. Improve test performance (parallel execution, reduced mock overhead)
5. Increase test coverage to >= 90%

## Scope

- Round-trip test coverage for all 76 newave + 150 nwlistop file handlers
- Version-specific tests for files with VERSIONS dictionaries
- Validation tests for versioned files
- Test infrastructure improvements (conftest.py, fixtures, parallelism)

## Tickets (Refined)

| Ticket     | Title                                                           | Effort   | Detail Level |
| ---------- | --------------------------------------------------------------- | -------- | ------------ |
| ticket-027 | Add round-trip tests for newave file handlers                   | 3 points | Refined      |
| ticket-028 | Add round-trip tests for nwlistop file handlers                 | 5 points | Refined      |
| ticket-029 | Add version-aware and validation tests                          | 1 point  | Refined      |
| ticket-030 | Optimize test execution (parallel, fixtures, mock improvements) | 2 points | Refined      |

## Current State Summary (at refinement time)

- **Test baseline**: 1134 tests, 41.32s wall-clock (sequential)
- **Newave round-trip coverage**: 31 of 64 test files have `test_leitura_escrita_*` tests
- **Nwlistop round-trip coverage**: 0 of 172 handler test files have file-level round-trip tests (block-level coverage exists in 2 base class test files)
- **Version/validation tests**: 8 tests in `test_version_validate.py` covering 3 of 5 versioned handlers (Cmarg, Pivarm, AvlCortesFpha)
- **No conftest.py** files exist; no pytest-xdist for parallel execution
- **Expected test count after epic**: ~1310+ tests

## Dependencies

- **Blocked By**: Epic 03 (version tests depend on VERSIONS), Epic 02 (TabularSection changes affect test patterns) -- both completed
- **Blocks**: None
