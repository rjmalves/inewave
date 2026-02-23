# ticket-018 Write version-aware tests for versioned file classes

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Create comprehensive tests that exercise the `read(version=...)` and `validate()` APIs on all file classes that have `VERSIONS` dictionaries. Tests should verify that version-specific block/section lists are correctly resolved, that DataFrames have the expected columns for each version, and that `validate()` returns correct `VersionMatchResult` objects.

## Anticipated Scope

- **Files likely to be modified**: Test files in `tests/newave/` and `tests/nwlistop/` for each versioned file class; possibly new mock data files for different versions
- **Key decisions needed**: Whether to create version-specific mock data or reuse existing mocks with version parameters; test naming conventions for version tests
- **Open questions**:
  - Do we have real sample files for multiple NEWAVE versions to use as test fixtures?
  - Should version tests be in separate test files or appended to existing test files?
  - What coverage target should we aim for on version-specific code paths?

## Dependencies

- **Blocked By**: ticket-015, ticket-016, ticket-017
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
