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

## Tickets (Outline)

| Ticket     | Title                                                           | Effort   |
| ---------- | --------------------------------------------------------------- | -------- |
| ticket-027 | Add round-trip tests for newave file handlers                   | 3 points |
| ticket-028 | Add round-trip tests for nwlistop file handlers                 | 5 points |
| ticket-029 | Add version-aware and validation tests                          | 3 points |
| ticket-030 | Optimize test execution (parallel, fixtures, mock improvements) | 3 points |

## Dependencies

- **Blocked By**: Epic 03 (version tests depend on VERSIONS), Epic 02 (TabularSection changes affect test patterns)
- **Blocks**: None
