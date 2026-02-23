# ticket-030 Optimize test execution (parallel, fixtures, mock improvements)

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Improve test execution speed and developer experience for the 430+ test suite. The current test suite uses `unittest.mock.patch` on `builtins.open` for every test, which may be slow for large mock datasets. Investigate and implement improvements: pytest-xdist for parallel execution, shared fixtures for common mock data, and potential simplification of mock patterns after the TabularSection migration.

## Anticipated Scope

- **Files likely to be modified**: `conftest.py` files, `pyproject.toml` (pytest configuration, optional deps), test fixture organization
- **Key decisions needed**: Whether to add pytest-xdist to dev dependencies; whether to refactor mock_open patterns to use fixtures; whether to share mock data across related tests
- **Open questions**:
  - What is the current test suite execution time?
  - Are there test isolation issues that prevent parallel execution?
  - After the TabularSection migration, are the mock patterns simpler (dict-of-lists instead of raw text)?
  - Would conftest.py session-scoped fixtures for mock data improve performance?

## Dependencies

- **Blocked By**: ticket-013
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
