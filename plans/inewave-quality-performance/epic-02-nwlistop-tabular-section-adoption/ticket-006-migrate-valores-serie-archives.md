# ticket-006 Migrate ValoresSerie archive base classes to use TabelaSerieAnual

## Context

### Background

After ticket-004 creates the `TabelaSerieAnual` base class, the archive base classes that use `ValoresSerie` blocks need to be updated to work with both the old and new block types, and eventually transition fully to `TabelaSerieAnual`.

There are 5 archive base classes that use `ValoresSerie` blocks:

1. `ArquivoREE` (16 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivoree.py`
2. `ArquivoSIN` (19 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivosin.py`
3. `ArquivoUsina` (17 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivousina.py`
4. `ArquivoSubmercado` -- `inewave/nwlistop/modelos/arquivos/arquivosubmercado.py`
5. `ArquivoRestricao` (4 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivorestricao.py`

All 5 implement the same pattern:

```python
def __monta_tabela(self) -> pd.DataFrame:
    df = None
    for b in self.data.of_type(ValoresSerie):
        dados = b.data
        if dados is None:
            continue
        elif df is None:
            df = b.data
        else:
            df = pd.concat([df, b.data], ignore_index=True)
    return df
```

### Relation to Epic

This ticket bridges the gap between the new base classes (ticket-004) and the batch model file migrations (tickets 008-009). It ensures the archive infrastructure works with `TabelaSerieAnual` blocks.

### Current State

Each archive base class:

1. Inherits from `BlockFile`
2. Declares `BLOCKS = [HeaderBlock, ValoresSerie]` (where HeaderBlock is REE, SIN, Usina, etc.)
3. Has `__monta_tabela()` that iterates over `ValoresSerie` blocks and concatenates DataFrames
4. Exposes `.valores` property returning `Optional[pd.DataFrame]`
5. May expose an entity property (`.ree`, `.submercado`, `.usina`)

## Specification

### Requirements

1. Update each of the 5 archive base classes to accept both `ValoresSerie` and `TabelaSerieAnual` blocks
2. The `__monta_tabela()` method must work identically regardless of which block type is used
3. Since both `ValoresSerie` and `TabelaSerieAnual` produce the same DataFrame in `.data`, the `__monta_tabela()` can use a common base type for iteration
4. Make `TabelaSerieAnual` a recognized subtype so `self.data.of_type()` works correctly
5. All existing tests must pass without modification

### Inputs/Props

No public API changes.

### Outputs/Behavior

- `.valores` property returns the same `Optional[pd.DataFrame]` as before
- Entity properties (`.ree`, `.submercado`, `.usina`) unchanged
- Both old `ValoresSerie` blocks and new `TabelaSerieAnual` blocks are handled

### Error Handling

No changes to error handling.

## Acceptance Criteria

- [ ] Given `ArquivoREE` with `TabelaSerieAnual` blocks, when I call `.valores`, then I get the same DataFrame as with `ValoresSerie` blocks
- [ ] Given `ArquivoSIN` with `TabelaSerieAnual` blocks, when I call `.valores`, then I get the same DataFrame
- [ ] Given all existing tests for ArquivoREE subclasses (earmf, eaf, evert, etc.), when I run them, then they all pass
- [ ] Given the 5 archive base class files, when I read them, then they support both block types

## Implementation Guide

### Suggested Approach

The key insight: `TabelaSerieAnual` extends `Block` and produces a DataFrame in `.data`, just like `ValoresSerie`. The `__monta_tabela()` method iterates using `self.data.of_type(SomeBlockType)`. The simplest approach is:

**Option A (minimal change)**: Make `TabelaSerieAnual` a subclass of `ValoresSerie` (so `of_type(ValoresSerie)` catches both). This is the least disruptive but creates a misleading inheritance hierarchy.

**Option B (clean approach)**: Change `of_type()` calls to iterate over a common base type, or use a protocol/ABC. Since both classes extend `Block`, we can iterate over all non-header blocks.

**Recommended: Option B**, using a helper method:

```python
def __monta_tabela(self) -> pd.DataFrame:
    df = None
    for b in self.data:
        if isinstance(b, (ValoresSerie, TabelaSerieAnual)):
            dados = b.data
            if dados is None:
                continue
            elif df is None:
                df = b.data
            else:
                df = pd.concat([df, b.data], ignore_index=True)
    return df
```

Or even simpler -- during the transition, the BLOCKS list determines which type is used, so `of_type` already works correctly. The archive base class just needs to accept whatever block type produces DataFrames.

### Key Files to Modify

1. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivoree.py`
2. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivosin.py`
3. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivousina.py`
4. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivosubmercado.py`
5. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivorestricao.py`

### Patterns to Follow

- Keep the lazy property pattern (`__valores` cache)
- Keep the `pd.concat` aggregation pattern
- Import both block types and use `isinstance` for the transition period

### Pitfalls to Avoid

- Do NOT change the public property signatures
- Do NOT change how entity properties (.ree, .submercado, .usina) work
- Do NOT remove the `ValoresSerie` import yet -- it is still used by non-migrated model files
- Ensure `of_type()` or `isinstance()` works correctly with the cfinterface data container's type index

## Testing Requirements

### Unit Tests

No new tests needed -- existing tests for all archive subclasses serve as regression tests.

### Integration Tests

Run `pytest tests/nwlistop/ -x` to verify all nwlistop tests pass.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-004
- **Blocks**: ticket-008, ticket-009

## Effort Estimate

**Points**: 3
**Confidence**: High
