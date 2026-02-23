# ticket-025 Reduce code duplication in nwlistop archive base classes

## Context

### Background

The nwlistop module has 13 archive base classes in `inewave/nwlistop/modelos/arquivos/`. These classes all extend `cfinterface.files.blockfile.BlockFile` and share nearly identical implementations of `__init__`, `__monta_tabela`, and a `valores` property. The only differences are: (a) which header block type is used (REE, Submercado, Usina, Restricao, ParSubmercados, EstacaoBombeamento, or none for SIN variants), (b) which data block types are checked in `isinstance()` (ValoresSerie/TabelaSerieAnual for non-patamar, ValoresSeriePatamar/TabelaSeriePatamarAnual for patamar, ValoresClasseTermicaSeriePatamar/TabelaSeriePatamarAnual for the classe termica variant), and (c) the entity-specific property (`.ree`, `.submercado`, `.usina`, `.restricao`, `.estacao`, `.submercado_de`/`.submercado_para`, or none for SIN).

This duplication was explicitly called out in the Epic 05 overview as a deduplication target. After the mypy strict annotations from tickets 023-024, the duplication is well-typed and ready for structural refactoring.

### Relation to Epic

This ticket addresses goal #3 of Epic 05: "Reduce code duplication in nwlistop models and archive base classes." It is independent from the mypy strict work (tickets 023-024) and can be executed in parallel, but is ordered after them because the type annotations added in those tickets make the refactoring safer and more clearly expressed.

### Current State

The 13 archive base files are:

**Non-patamar (series-only) archives (5 files):**

1. `arquivoree.py` -- ArquivoREE (header: REE, data: ValoresSerie/TabelaSerieAnual, entity: `.ree`)
2. `arquivosubmercado.py` -- ArquivoSubmercado (header: Submercado, data: ValoresSerie/TabelaSerieAnual, entity: `.submercado`)
3. `arquivousina.py` -- ArquivoUsina (header: Usina, data: ValoresSerie/TabelaSerieAnual, entity: `.usina`)
4. `arquivorestricao.py` -- ArquivoRestricao (header: Restricao, data: ValoresSerie/TabelaSerieAnual, entity: `.restricao`)
5. `arquivosin.py` -- ArquivoSIN (no header block, data: ValoresSerie/TabelaSerieAnual, no entity property)

**Patamar archives (7 files):** 6. `arquivoreepatamar.py` -- ArquivoREEPatamar (header: REE, data: ValoresSeriePatamar/TabelaSeriePatamarAnual, entity: `.ree`) 7. `arquivosubmercadopatamar.py` -- ArquivoSubmercadoPatamar (header: Submercado, data: ValoresSeriePatamar/TabelaSeriePatamarAnual, entity: `.submercado`) 8. `arquivousinapatamar.py` -- ArquivoUsinaPatamar (header: Usina, data: ValoresSeriePatamar/TabelaSeriePatamarAnual, entity: `.usina`) 9. `arquivorestricaopatamar.py` -- ArquivoRestricaoPatamar (header: Restricao, data: ValoresSeriePatamar/TabelaSeriePatamarAnual, entity: `.restricao`) 10. `arquivosinpatamar.py` -- ArquivoSINPatamar (no header block, data: ValoresSeriePatamar/TabelaSeriePatamarAnual, no entity property) 11. `arquivoestacaobombeamentopatamar.py` -- ArquivoEstacaoBombeamentoPatamar (header: EstacaoBombeamento, data: ValoresSeriePatamar/TabelaSeriePatamarAnual, entity: `.estacao`) 12. `arquivoparsubmercadopatamar.py` -- ArquivoParSubmercadoPatamar (header: ParSubmercados, data: ValoresSeriePatamar/TabelaSeriePatamarAnual, entities: `.submercado_de` + `.submercado_para`)

**Classe termica archive (1 file):** 13. `arquivoclassetermicasubmercadopatamar.py` -- ArquivoClasseTermicaSubmercadoPatamar (header: Submercado, data: ValoresClasseTermicaSeriePatamar/TabelaSeriePatamarAnual, entity: `.submercado`)

Each file is 53-81 lines. The `__monta_tabela` method body is identical across all 13 files except for the `isinstance()` type check. The `__init__` method body is identical in all 13. The `valores` property body is identical in all 13. Only the entity-specific properties differ (and `ArquivoParSubmercadoPatamar` has two entity properties instead of one).

Total duplicated code: approximately 650 lines that could be reduced to ~100 lines of base class + 13 small subclass declarations.

## Specification

### Requirements

1. Create two abstract mixin or intermediate base classes that encapsulate the shared logic:
   - One for non-patamar archives (series-only data blocks)
   - One for patamar archives (series+patamar data blocks)
2. Refactor all 13 archive base classes to use the new shared base(s)
3. The public API of each archive class must remain identical: same class names, same property names, same return types
4. All 170+ handler classes that inherit from these 13 base classes must continue to work without modification
5. All 1134 existing tests must pass
6. The `isinstance()` dual-type guard pattern must be preserved for forward compatibility (learnings: "isinstance() dual-type guard in archive bases")

### Design: Two Intermediate Base Classes

Create two new files in `inewave/nwlistop/modelos/arquivos/`:

**`_base_serie.py`** -- Base class for non-patamar archives:

```python
from typing import Any, Optional, Type
import pandas as pd
from cfinterface.components.block import Block
from cfinterface.files.blockfile import BlockFile
from inewave.nwlistop.modelos.blocos.tabela_serie_anual import TabelaSerieAnual
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class _ArquivoSerieBase(BlockFile):
    """
    Internal base class for nwlistop archive files with series-only
    tabular data. Subclasses must set BLOCKS.
    """
    __slots__ = ["__valores"]

    # Subclasses override these if they have a header block
    _HEADER_BLOCK: Optional[Type[Block]] = None
    _DATA_BLOCK_TYPES: tuple = (ValoresSerie, TabelaSerieAnual)

    def __init__(self, data: Any = ...) -> None:
        super().__init__(data)
        self.__valores: Optional[pd.DataFrame] = None

    def _monta_tabela(self) -> Optional[pd.DataFrame]:
        dfs = [
            b.data
            for b in self.data
            if isinstance(b, self._DATA_BLOCK_TYPES)
            and b.data is not None
        ]
        if not dfs:
            return None
        return pd.concat(dfs, ignore_index=True)

    @property
    def valores(self) -> Optional[pd.DataFrame]:
        if self.__valores is None:
            self.__valores = self._monta_tabela()
        return self.__valores

    def _get_header_value(self) -> Any:
        """Returns the header block's data, or None."""
        if self._HEADER_BLOCK is None:
            return None
        b = self.data.get_blocks_of_type(self._HEADER_BLOCK)
        if isinstance(b, self._HEADER_BLOCK):
            return b.data
        return None
```

**`_base_serie_patamar.py`** -- Base class for patamar archives:

```python
# Same structure but _DATA_BLOCK_TYPES = (ValoresSeriePatamar, TabelaSeriePatamarAnual)
```

Then each archive class becomes a thin subclass:

```python
class ArquivoREE(_ArquivoSerieBase):
    _HEADER_BLOCK = REE
    BLOCKS = [REE, ValoresSerie]

    @property
    def ree(self) -> Optional[str]:
        return self._get_header_value()
```

**Special cases:**

- `ArquivoSIN` and `ArquivoSINPatamar` have no header block and no entity property. They inherit the base directly with `_HEADER_BLOCK = None`.
- `ArquivoParSubmercadoPatamar` has two entity properties that access `b.data[0]` and `b.data[1]`. Its entity properties are custom but still use `_get_header_value()`-like logic.
- `ArquivoClasseTermicaSubmercadoPatamar` uses `ValoresClasseTermicaSeriePatamar` instead of `ValoresSeriePatamar` in the isinstance check. Override `_DATA_BLOCK_TYPES` for this one.
- `ArquivoRestricao` and `ArquivoRestricaoPatamar` return `Optional[int]` from their entity property (not `Optional[str]`).

### Inputs/Props

No new public APIs. The base classes are internal (`_` prefix).

### Outputs/Behavior

The public behavior of all 13 archive classes and their 170+ handler subclasses remains identical:

- Same class names
- Same `valores` property returning `Optional[pd.DataFrame]`
- Same entity-specific properties (`.ree`, `.submercado`, `.usina`, `.restricao`, `.estacao`, `.submercado_de`, `.submercado_para`)
- Same `BLOCKS` class attribute

### Error Handling

No changes to error handling. The `_monta_tabela` method preserves the existing behavior of returning `None` when no data blocks are found.

## Acceptance Criteria

- [ ] Given the 13 archive base files, when counting total non-blank lines, then the total is at least 30% less than the current ~830 lines
- [ ] Given any archive subclass (e.g., `ArquivoREE`), when inspecting its source, then it delegates `__monta_tabela`/`valores` logic to the shared base class
- [ ] Given the handler class `Earmf` (which inherits from `ArquivoREE`), when reading a test file, then `obj.valores` returns the same DataFrame as before the refactor
- [ ] Given the handler class `Cmarg` (which inherits from `ArquivoREEPatamar`), when reading a test file, then `obj.valores` returns the same DataFrame as before the refactor
- [ ] Given any handler class inheriting from any of the 13 archive bases, when running its tests, then all tests pass unchanged
- [ ] Given the full test suite, when running `pytest`, then all 1134 tests pass
- [ ] Given the refactored code, when running `mypy inewave/nwlistop/ --strict`, then 0 errors are reported (maintains strict compliance from ticket-024)
- [ ] Given `ArquivoParSubmercadoPatamar`, when inspecting it, then `.submercado_de` and `.submercado_para` properties still work correctly
- [ ] Given `ArquivoClasseTermicaSubmercadoPatamar`, when inspecting it, then the `isinstance()` check uses `ValoresClasseTermicaSeriePatamar` (not `ValoresSeriePatamar`)

## Implementation Guide

### Suggested Approach

1. **Create `_base_serie.py`**: Implement `_ArquivoSerieBase` with `_monta_tabela`, `valores` property, `_get_header_value` method. Use `_HEADER_BLOCK` and `_DATA_BLOCK_TYPES` class variables for configuration.

2. **Create `_base_serie_patamar.py`**: Implement `_ArquivoSeriePatamarBase` with the same pattern but using `(ValoresSeriePatamar, TabelaSeriePatamarAnual)` as default data block types.

3. **Refactor the 5 non-patamar archives** one at a time:
   - `ArquivoSIN` (simplest, no header)
   - `ArquivoREE`, `ArquivoSubmercado`, `ArquivoUsina`, `ArquivoRestricao`

4. **Run `pytest` after each refactored file** to catch regressions early.

5. **Refactor the 7 patamar archives** one at a time:
   - `ArquivoSINPatamar` (simplest, no header)
   - `ArquivoREEPatamar`, `ArquivoSubmercadoPatamar`, `ArquivoUsinaPatamar`, `ArquivoRestricaoPatamar`, `ArquivoEstacaoBombeamentoPatamar`
   - `ArquivoParSubmercadoPatamar` (special: two entity properties)

6. **Refactor `ArquivoClasseTermicaSubmercadoPatamar`** (special: different data block types).

7. **Run full test suite** and `mypy inewave/nwlistop/ --strict`.

### Key Files to Modify

- **New**: `inewave/nwlistop/modelos/arquivos/_base_serie.py`
- **New**: `inewave/nwlistop/modelos/arquivos/_base_serie_patamar.py`
- **Modify**: All 13 files in `inewave/nwlistop/modelos/arquivos/arquivo*.py`

### Patterns to Follow

- **`isinstance()` dual-type guard**: Must be preserved. Use `_DATA_BLOCK_TYPES` tuple as the argument to `isinstance()`. See learnings: "isinstance(b, (ValoresSerie, TabelaSerieAnual))".
- **`__slots__` on every subclass**: Learnings: "`__slots__ = []` on every block subclass".
- **Collect-then-concat**: Learnings: "All 13 archive base classes now use a list comprehension to collect DataFrames, then call pd.concat(dfs, ignore_index=True) once."
- **Private names with `_` prefix**: The base classes are internal implementation details. Use `_ArquivoSerieBase` and `_ArquivoSeriePatamarBase` naming.
- **`__monta_tabela` becomes `_monta_tabela`**: The double-underscore name-mangled method `__monta_tabela` is currently per-class. In the shared base, use single-underscore `_monta_tabela` so subclasses can access it if needed.

### Pitfalls to Avoid

- **Do NOT change any public class names** or property names. These are part of the library's public API.
- **Do NOT merge the two base classes into one** using a boolean flag like `is_patamar`. The type separation (series vs series+patamar) is fundamental and should remain in the class hierarchy.
- **Do NOT use a metaclass or factory function**. The straightforward inheritance approach is simpler and more maintainable. The learnings warn: "Plan for a cleanup pass after batch migrations" -- keep the design simple.
- **Do NOT change `BLOCKS` class attribute** on any subclass. Handler classes override `BLOCKS` with their specific block types and the base class `BLOCKS` is just a default.
- **`__slots__` mangling**: The private `__valores` attribute uses name mangling (`_ArquivoSerieBase__valores`). When moving from `ArquivoREE.__valores` to `_ArquivoSerieBase.__valores`, the mangled name changes. This means subclasses cannot access `self.__valores` directly -- they use the `valores` property instead, which is correct.
- **`ArquivoParSubmercadoPatamar`** accesses `b.data[0]` and `b.data[1]` for its two entity properties. This cannot use `_get_header_value()` directly. Either add a `_get_header_data()` that returns the raw data, or keep custom property implementations for this one class.

## Testing Requirements

### Unit Tests

No new tests. The existing 1134 tests cover all 13 archive base classes through their handler subclasses.

### Integration Tests

Run `mypy inewave/nwlistop/ --strict` to verify type safety is maintained.

### E2E Tests (if applicable)

Not applicable.

## Dependencies

- **Blocked By**: ticket-013 (completed -- deprecated blocks cleaned up)
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High -- the 13 files are nearly identical and the refactoring pattern is straightforward extraction of a base class. The design is well-constrained by the existing public API.
