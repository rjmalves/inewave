# ticket-024 Fix mypy strict mode errors in nwlistop module

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Extend mypy strict mode to the `inewave/nwlistop/` module and fix all resulting type errors. The nwlistop module is the largest (~346 files), so this is expected to be the most time-consuming type safety ticket. After the TabularSection migration (Epic 02), many of the old type issues around numpy arrays and manual DataFrame construction should be eliminated.

## Anticipated Scope

- **Files likely to be modified**: All files in `inewave/nwlistop/` that produce strict-mode errors, plus the new `TabelaSerieAnual` and `TabelaSeriePatamarAnual` base classes
- **Key decisions needed**: Whether to fix all errors in one pass or incrementally enable strict sub-options
- **Open questions**:
  - How many errors remain after Epic 02's TabularSection migration?
  - Are the archive base classes the primary source of type issues, or the model files?
  - Can generic typing be applied to archive base classes (e.g., `ArquivoREE[TBlockType]`)?

## Dependencies

- **Blocked By**: ticket-023
- **Blocks**: ticket-026

## Effort Estimate

**Points**: 5
**Confidence**: Low (will be re-estimated during refinement)
