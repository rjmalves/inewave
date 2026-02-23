# ticket-020 Optimize DataFrame creation in archive base classes

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Optimize the DataFrame creation pattern in the 13 nwlistop archive base classes. The current pattern uses repeated `pd.concat()` in a loop, which is O(n^2) for n year blocks. Replace with a single bulk construction (e.g., collect all dict-of-lists and build DataFrame once). After the TabularSection migration, blocks produce dict-of-lists that can be merged more efficiently.

## Anticipated Scope

- **Files likely to be modified**: All 13 archive base classes in `inewave/nwlistop/modelos/arquivos/`, specifically their `__monta_tabela()` methods
- **Key decisions needed**: Whether to use `pd.concat([list_of_dfs])` (single call) or merge dict-of-lists before DataFrame construction; whether `TabularParser.to_dataframe()` should be used
- **Open questions**:
  - After the TabularSection migration, does `self.data` on each block return a DataFrame or a dict-of-lists? This determines the optimal aggregation strategy.
  - How significant is the `pd.concat` overhead for typical file sizes (5-30 year blocks)?
  - Should we preserve the lazy property pattern or switch to eager evaluation?

## Dependencies

- **Blocked By**: ticket-019
- **Blocks**: ticket-022

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
