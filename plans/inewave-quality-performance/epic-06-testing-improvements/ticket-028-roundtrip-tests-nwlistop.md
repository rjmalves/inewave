# ticket-028 Add round-trip tests for nwlistop file handlers

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Add round-trip tests for all 150+ nwlistop file handlers. After the TabularSection migration (Epic 02), the write path is provided by `TabelaSerieAnual`/`TabelaSeriePatamarAnual` base classes, which delegate to `TabularParser.format_rows()`. Round-trip tests verify that the new TabularSection-based write produces output that re-reads identically.

## Anticipated Scope

- **Files likely to be modified**: All ~170 test files in `tests/nwlistop/` (adding round-trip test functions)
- **Key decisions needed**: Whether to test round-trip at block level (individual year blocks) or file level (full file read -> write -> read); batch test generation strategy for 150+ files
- **Open questions**:
  - After the TabularSection migration, does `TabelaSerieAnual.write()` produce output compatible with `TabelaSerieAnual.read()`?
  - Can a parametrized test fixture cover all nwlistop file types, or do they need individual tests?
  - Should round-trip tests be strict (byte-identical) or semantic (DataFrame-equal)?

## Dependencies

- **Blocked By**: ticket-013
- **Blocks**: None

## Effort Estimate

**Points**: 5
**Confidence**: Low (will be re-estimated during refinement)
