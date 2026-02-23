# ticket-027 Add round-trip tests for newave file handlers

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Add round-trip tests (read -> write -> read -> compare) for all 76 newave file handlers. Currently many tests only verify that read produces non-None values. Round-trip tests ensure that write produces output that can be re-read to produce identical data, which is critical for file integrity.

## Anticipated Scope

- **Files likely to be modified**: All test files in `tests/newave/` (adding new test functions to existing files)
- **Key decisions needed**: Whether to use in-memory StringIO/BytesIO for round-trip or write to temp files; comparison strategy (DataFrame.equals for tabular, attribute equality for scalar)
- **Open questions**:
  - How many newave handlers currently lack round-trip tests?
  - Do all file types support write operations, or are some read-only?
  - For binary files (STORAGE=BINARY), does write produce byte-identical output?

## Dependencies

- **Blocked By**: ticket-013
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
