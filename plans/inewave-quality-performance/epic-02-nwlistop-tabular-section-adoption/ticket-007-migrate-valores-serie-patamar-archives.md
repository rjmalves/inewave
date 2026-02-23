# ticket-007 Migrate ValoresSeriePatamar archive base classes to use TabelaSeriePatamarAnual

## Context

### Background

After ticket-005 creates the `TabelaSeriePatamarAnual` base class, the archive base classes that use `ValoresSeriePatamar` blocks need to be updated. This is the patamar-variant counterpart of ticket-006.

There are 8 archive base classes that use `ValoresSeriePatamar` blocks:

1. `ArquivoSubmercadoPatamar` (35 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivosubmercadopatamar.py`
2. `ArquivoUsinaPatamar` (25 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivousinapatamar.py`
3. `ArquivoSINPatamar` (22 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivosinpatamar.py`
4. `ArquivoREEPatamar` (12 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivoreepatamar.py`
5. `ArquivoRestricaoPatamar` (8 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivorestricaopatamar.py`
6. `ArquivoEstacaoBombeamentoPatamar` (2 subclasses) -- `inewave/nwlistop/modelos/arquivos/arquivoestacaobombeamentopatamar.py`
7. `ArquivoClasseTermicaSubmercadoPatamar` (1 subclass) -- `inewave/nwlistop/modelos/arquivos/arquivoclassetermicasubmercadopatamar.py`
8. `ArquivoPARSubmercadoPatamar` (1 subclass) -- `inewave/nwlistop/modelos/arquivos/arquivoparsubmercadopatamar.py`

All implement the same `__monta_tabela()` pattern with `pd.concat`, identical to the ValoresSerie archives but iterating over `ValoresSeriePatamar`.

### Relation to Epic

This ticket parallels ticket-006 for the patamar block hierarchy. Together, tickets 006 and 007 prepare ALL 13 archive base classes for the batch model file migrations.

### Current State

Same pattern as ticket-006's archives, but with patamar dimension:

- `BLOCKS = [HeaderBlock, ValoresSeriePatamar]`
- `__monta_tabela()` iterates `self.data.of_type(ValoresSeriePatamar)`
- `.valores` returns DataFrame with patamar column
- Additional entity properties (`.submercado`, `.ree`, `.usina`, `.restricao`, `.estacao_bombeamento`)

## Specification

### Requirements

1. Update all 8 patamar archive base classes to accept both `ValoresSeriePatamar` and `TabelaSeriePatamarAnual` blocks
2. The `__monta_tabela()` method must work identically with either block type
3. All existing tests must pass without modification

### Inputs/Props

No public API changes.

### Outputs/Behavior

- `.valores` returns the same `Optional[pd.DataFrame]` (with patamar column)
- Entity properties unchanged
- Both old and new block types handled

### Error Handling

No changes.

## Acceptance Criteria

- [ ] Given `ArquivoSubmercadoPatamar` with `TabelaSeriePatamarAnual` blocks, when I call `.valores`, then I get the same DataFrame as with `ValoresSeriePatamar` blocks
- [ ] Given all existing tests for patamar archive subclasses (cmarg, cdef, deficit, etc.), when I run them, then they all pass
- [ ] Given the 8 archive base class files, when I read them, then they support both block types

## Implementation Guide

### Suggested Approach

Same approach as ticket-006: use `isinstance()` check for both old and new block types in `__monta_tabela()`, or leverage the fact that `of_type()` with `issubclass` matching will correctly handle the transition if the BLOCKS list is updated.

For `ArquivoClasseTermicaSubmercadoPatamar`, note that it uses `ValoresClasseTermicaSeriePatamar` (a special variant). This archive may need a separate treatment or the special variant needs its own `TabelaSerieAnual` equivalent. If the single subclass (`gtert`) is simple enough, handle it inline.

### Key Files to Modify

1. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivosubmercadopatamar.py`
2. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivousinapatamar.py`
3. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivosinpatamar.py`
4. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivoreepatamar.py`
5. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivorestricaopatamar.py`
6. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivoestacaobombeamentopatamar.py`
7. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivoclassetermicasubmercadopatamar.py`
8. `/home/rogerio/git/inewave/inewave/nwlistop/modelos/arquivos/arquivoparsubmercadopatamar.py`

### Patterns to Follow

Same as ticket-006.

### Pitfalls to Avoid

- The `ArquivoClasseTermicaSubmercadoPatamar` uses a different base block type (`ValoresClasseTermicaSeriePatamar`) -- do not assume it follows the exact same pattern
- Some patamar archives expose additional properties beyond `.valores` -- do not break them
- The patamar column may be `str` or `int` depending on the file type -- preserve the existing dtype

## Testing Requirements

### Unit Tests

No new tests -- existing tests serve as regression.

### Integration Tests

Run `pytest tests/nwlistop/ -x`.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-005
- **Blocks**: ticket-010, ticket-011, ticket-012

## Effort Estimate

**Points**: 3
**Confidence**: High
