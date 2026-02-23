# ticket-029 Add version-aware and validation tests

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Create comprehensive tests that exercise the version-aware read API (`read(version=...)`) and validation API (`validate()`) on all file classes with VERSIONS dictionaries. Tests verify correct version resolution, version-specific block/section selection, and validation result accuracy.

## Anticipated Scope

- **Files likely to be modified**: Test files for versioned file classes (list depends on Epic 03 outcomes), possibly new mock data for different versions
- **Key decisions needed**: Whether to create version-specific mock data files or parametrize existing mocks; test organization (version tests in existing files vs. dedicated version test file)
- **Open questions**:
  - How many file classes will have VERSIONS after Epic 03?
  - Do we have sample data for multiple NEWAVE versions?
  - Should tests verify the exact VersionMatchResult fields or just the `matched` boolean?

## Dependencies

- **Blocked By**: ticket-018 (Epic 03 version tests), ticket-013
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
