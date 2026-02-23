# ticket-025 Reduce code duplication in nwlistop archive base classes

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

After the TabularSection migration (Epic 02), identify remaining code duplication across the 13 nwlistop archive base classes and reduce it through shared abstractions. The 13 base classes currently have nearly identical `__monta_tabela()` methods, `__init__()` patterns, and property implementations. A single generic base class or mixin could eliminate this duplication.

## Anticipated Scope

- **Files likely to be modified**: All 13 files in `inewave/nwlistop/modelos/arquivos/`, possibly creating a new shared base class or mixin
- **Key decisions needed**: Whether to use a single generic base class parameterized by header block type, or a mixin approach, or template method pattern
- **Open questions**:
  - After Epic 02, how much code remains duplicated across the 13 archive base classes?
  - Is the only difference the header block type (REE, SIN, Usina, etc.) and the entity property name (.ree, .submercado, .usina)?
  - Would a factory function or metaclass approach be cleaner than inheritance?

## Dependencies

- **Blocked By**: ticket-013
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
