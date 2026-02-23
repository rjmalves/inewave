# ticket-016 Add VERSIONS dictionaries to nwlistop BlockFile classes

## Context

### Background

The nwlistop module contains 120+ handler classes for NEWAVE output files produced by the NWLISTOP post-processor. These handlers extend archive base classes (`ArquivoREE`, `ArquivoUsina`, `ArquivoSubmercado`, `ArquivoSubmercadoPatamar`, etc.) which in turn extend `BlockFile`. After Epic 02, all nwlistop model files use the `TabelaSerieAnual` or `TabelaSeriePatamarAnual` base classes with `COLUMNS` definitions. Version differences in these files manifest as different `FloatField` sizes (e.g., width 8 vs 11) or different `format` parameters (e.g., decimal vs `format="E"` scientific notation).

Currently, only 4 nwlistop handler files have `VERSIONS` dictionaries:

- `inewave/nwlistop/cmarg.py` (keys `"27"`, `"29.4.1"`)
- `inewave/nwlistop/cmargmed.py` (keys `"28"`, `"29.4.1"`)
- `inewave/nwlistop/pivarm.py` (keys `"28.12"`, `"29.2"`)
- `inewave/nwlistop/pivarmincr.py` (keys `"28.12"`, `"29.2"`)

This ticket expands VERSIONS coverage to all nwlistop files identified in the version catalog (ticket-014) as having format differences between NEWAVE versions.

### Relation to Epic

This is the second of two core implementation tickets in Epic 03 (alongside ticket-015 for newave). Together, they ensure `read(version=...)` works across the entire inewave library.

### Current State

- All nwlistop model files define `TabelaSerieAnual` or `TabelaSeriePatamarAnual` subclasses with `COLUMNS = [ColumnDef(...), ...]`.
- The existing 4 VERSIONS files demonstrate the pattern: the handler file declares `BLOCKS = [HeaderBlock, LatestDataBlock]` and `VERSIONS = { "older_key": [HeaderBlock, OlderDataBlock], "newer_key": [HeaderBlock, NewerDataBlock] }`.
- Version-variant model classes differ only in their `COLUMNS` definitions -- typically `FloatField` width and/or `format` parameter.
- Archive base classes (`ArquivoREE`, `ArquivoUsina`, etc.) use `isinstance(b, (ValoresSerie, TabelaSerieAnual))` dual-type guards in `__monta_tabela()`, so they accept both old and new block types without modification.
- The `BLOCKS` list in archive base classes is `[HeaderBlock, ValoresSerie]` (uses the deprecated type). Concrete handler subclasses override this with their specific block types. This means VERSIONS only needs to be declared in the concrete handler files, not in the archive base classes.

## Specification

### Requirements

1. **Read the version catalog** produced by ticket-014 at `plans/inewave-quality-performance/version-catalog.md` to get the definitive list of nwlistop files that need `VERSIONS`.
2. **For each nwlistop handler identified in the catalog** that does not already have VERSIONS, add a `VERSIONS` class-level dictionary.
3. **Create version-variant model classes** in the corresponding model file when needed. These are `TabelaSerieAnual` or `TabelaSeriePatamarAnual` subclasses with different `COLUMNS` definitions.
4. **Version-variant model classes** must:
   - Extend the same base class as the default model class (`TabelaSerieAnual` or `TabelaSeriePatamarAnual`)
   - Declare `__slots__ = []`
   - Define `COLUMNS` with the version-specific field sizes/formats
   - Follow the naming convention: `FooAnos` (latest), `FooAnos27` or `FooAnos_v29_2` (version-specific)
5. **The `BLOCKS` attribute must remain the latest/default version** for backward compatibility.
6. **Do not modify archive base classes** (`ArquivoREE`, `ArquivoUsina`, etc.) -- they already handle both old and new block types.

### Inputs/Props

- The version catalog at `plans/inewave-quality-performance/version-catalog.md` (produced by ticket-014)
- Existing nwlistop handler files in `inewave/nwlistop/`
- Existing nwlistop model files in `inewave/nwlistop/modelos/`
- Existing VERSIONS examples in cmarg.py, cmargmed.py, pivarm.py, pivarmincr.py

### Outputs/Behavior

For each affected handler file, add VERSIONS following this pattern:

```python
# inewave/nwlistop/somefile.py
from inewave.nwlistop.modelos.somefile import SomeAnos, SomeAnos27
from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import ArquivoSubmercado


class Somefile(ArquivoSubmercado):
    BLOCKS = [Submercado, SomeAnos]  # latest/default

    VERSIONS = {
        "27": [Submercado, SomeAnos27],
        "29.4.1": [Submercado, SomeAnos],
    }
```

For each new version-variant model class:

```python
# inewave/nwlistop/modelos/somefile.py
from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.tabular import ColumnDef

from inewave.config import MESES_DF
from inewave.nwlistop.modelos.blocos.tabela_serie_anual import TabelaSerieAnual


class SomeAnos27(TabelaSerieAnual):
    __slots__ = []
    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(8, 8 + 9 * i, 1))  # older, narrower
        for i in range(len(MESES_DF))
    ]


class SomeAnos(TabelaSerieAnual):
    __slots__ = []
    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(11, 8 + 11 * i, 2))  # latest, wider
        for i in range(len(MESES_DF))
    ]
```

### Error Handling

- cfinterface handles version resolution fallback automatically (falls back to default BLOCKS with a warning if no matching version key is found). No custom error handling needed in handler files.

## Acceptance Criteria

- [ ] Given the version catalog lists N nwlistop files as needing VERSIONS (beyond the existing 4), when inspecting the modified handler files, then all N files have a `VERSIONS` dictionary with the version keys specified in the catalog.
- [ ] Given a newly versioned nwlistop handler, when calling `Handler.read(path, version="<oldest_key>")` with appropriate test data, then the older block class (with different COLUMNS) is used for parsing.
- [ ] Given a newly versioned nwlistop handler, when calling `Handler.read(path)` (no version), then the default `BLOCKS` list is used (backward compatible).
- [ ] Given every new version-variant model class, when inspecting it, then it: (a) extends `TabelaSerieAnual` or `TabelaSeriePatamarAnual`, (b) declares `__slots__ = []`, (c) defines `COLUMNS` with version-specific field parameters.
- [ ] Given no behavioral changes to default code paths, when running `pytest`, then the full test suite (1126+ tests) passes.
- [ ] Given the 4 previously versioned files (cmarg, cmargmed, pivarm, pivarmincr), when inspecting them, then their existing `VERSIONS` dictionaries are unchanged.

## Implementation Guide

### Suggested Approach

1. Read the version catalog (`plans/inewave-quality-performance/version-catalog.md`) and identify all nwlistop files in the "Needs VERSIONS -- nwlistop BlockFile" section.
2. Group the files by archive base class (ArquivoREE, ArquivoUsina, ArquivoSubmercado, ArquivoSubmercadoPatamar, etc.) to batch similar changes.
3. For each file:
   a. Open the model file (e.g., `inewave/nwlistop/modelos/earmf.py`).
   b. If a version-variant model class does not exist, create it with the version-specific COLUMNS. Use the existing class as the template and adjust FloatField sizes/formats.
   c. Open the handler file (e.g., `inewave/nwlistop/earmf.py`).
   d. Import the version-variant model class.
   e. Add the `VERSIONS` dictionary.
4. Run `pytest` after each batch to catch regressions early.
5. Run `ruff check inewave/nwlistop/` and `ruff format inewave/nwlistop/`.

### Key Files to Modify

The exact list comes from the ticket-014 catalog. The handler files are in `inewave/nwlistop/` and their model files in `inewave/nwlistop/modelos/`. Reference patterns:

- **Handler with VERSIONS**: `inewave/nwlistop/cmarg.py` (handler pattern), `inewave/nwlistop/pivarm.py` (handler pattern)
- **Model with version-variant classes**: `inewave/nwlistop/modelos/cmarg.py` (two classes: `CmargsAnos27`, `CmargsAnos`), `inewave/nwlistop/modelos/pivarm.py` (two classes: `PivarmAnos`, `PivarmAnos_v29_2`)
- **Archive base classes** (read-only reference, do NOT modify): `inewave/nwlistop/modelos/arquivos/arquivoree.py`, `arquivousina.py`, `arquivosubmercado.py`, `arquivosubmercadopatamar.py`, etc.

### Patterns to Follow

- **Model class pattern from `inewave/nwlistop/modelos/cmarg.py`**:
  - `CmargsAnos27`: `FloatField(8, 15 + 9 * i, 2)` -- 8-char wide, 9-char stride
  - `CmargsAnos`: `FloatField(11, 14 + 11 * i, 2)` -- 11-char wide, 11-char stride
  - Both extend `TabelaSeriePatamarAnual`, both declare `__slots__ = []`
- **Model class pattern from `inewave/nwlistop/modelos/pivarm.py`**:
  - `PivarmAnos`: `FloatField(15, 7 + 15 * i, 2)` -- decimal format
  - `PivarmAnos_v29_2`: `FloatField(15, 7 + 15 * i, 7, format="E")` -- scientific notation
  - Both extend `TabelaSerieAnual`, both declare `__slots__ = []`
- **Handler pattern from `inewave/nwlistop/cmarg.py`**:
  ```python
  BLOCKS = [Submercado, CmargsAnos]
  VERSIONS = {
      "27": [Submercado, CmargsAnos27],
      "29.4.1": [Submercado, CmargsAnos],
  }
  ```
- **`COLUMNS` naming is load-bearing**: first entry must be `"serie"`, second (patamar variant) must be `"patamar"`, then 12 entries using `MESES_DF[i]`. Do not deviate from these names.

### Pitfalls to Avoid

- **Do not modify archive base classes** -- they already handle both old and new types via `isinstance()` dual-type guard.
- **Do not change existing VERSIONS on the 4 already-versioned files** unless the catalog explicitly calls for it.
- **COLUMNS field positions must be exact** -- the position (2nd argument to FloatField) and stride determine where each month's data is read from. Copy exact values from the catalog or from sample output files.
- **`__slots__ = []` is mandatory** on every new model class -- omitting it breaks the memory layout.
- **Do not rename existing classes** -- only add new version-variant classes alongside them.

## Testing Requirements

### Unit Tests

Existing tests must pass. No new tests in this ticket -- ticket-018 handles version-aware testing.

### Integration Tests

Not applicable.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-014 (provides the version catalog)
- **Blocks**: ticket-017, ticket-018

## Effort Estimate

**Points**: 3
**Confidence**: Medium (exact scope depends on ticket-014 catalog size)
