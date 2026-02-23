# ticket-008 Batch migrate ArquivoREE and ArquivoSIN model files to TabelaSerieAnual (35 files)

## Context

### Background

With `TabelaSerieAnual` created (ticket-004) and archive base classes updated (ticket-006), the actual model files can now be migrated. This ticket covers the 16 ArquivoREE subclasses and 19 ArquivoSIN subclasses -- all of which use `ValoresSerie`-derived blocks with the simple `[serie] + [12 monthly values]` pattern.

### Relation to Epic

This is the first batch migration ticket. It targets the simplest group: files that use `ValoresSerie` blocks without patamar.

### Current State

Each model file (e.g., `inewave/nwlistop/modelos/earmf.py`) contains a class like:

```python
class EarmsAnos(ValoresSerie):
    __slots__ = []
    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [IntegerField(4, 2)]
        + [FloatField(8, 8 + 9 * i, 1) for i in range(len(MESES_DF))]
    )
```

And the handler file (e.g., `inewave/nwlistop/earmf.py`) references it:

```python
class Earmf(ArquivoREE):
    BLOCKS = [REE, EarmsAnos]
```

## Specification

### Requirements

1. Convert each model file's block class from `ValoresSerie` subclass to `TabelaSerieAnual` subclass
2. Replace `HEADER_LINE` / `DATA_LINE` with `COLUMNS` (list of `ColumnDef`)
3. Update the handler file's `BLOCKS` list to reference the new class
4. Run the corresponding test for each file to verify backward compatibility

### Files to Migrate

**ArquivoREE subclasses (16 files):**
earmf, earmfp, eaf, eafb, edesvc, evert, evapo, perdf, invade, vmort, verturb, mevmin, vevmin, viol_evmin, valor_agua, vagua

**ArquivoSIN subclasses (19 files):**
earmfsin, earmfpsin, eafbsin, edesvcsin, evertsin, evaporsin, perdfsin, vmortsin, ctermsin, coper, custo_futuro, merclsin, mevminsin, vevminsin, verturbsin, viol_evminsin, c_v_rhv_s, c_v_rhq_s (Note: c_v_rhv_s and c_v_rhq_s use ArquivoSINPatamar, not ArquivoSIN -- these will be covered in ticket-011 instead. Adjust count accordingly.)

Correction: ArquivoSIN has 19 subclasses total. Verify exact list against codebase.

### Inputs/Props

Each model class currently defines `HEADER_LINE` and `DATA_LINE` as `Line` instances.

### Outputs/Behavior

Each model class now defines `COLUMNS` as a list of `ColumnDef`. The handler file's `BLOCKS` list references the migrated class. All tests pass identically.

### Error Handling

No behavioral changes.

## Acceptance Criteria

- [ ] Given all 35 model files, when I read them, then each uses `TabelaSerieAnual` as base class with `COLUMNS` definition
- [ ] Given all 35 handler files, when I read them, then `BLOCKS` references the migrated model class
- [ ] Given the test suite for these files, when I run `pytest tests/nwlistop/test_earmf.py tests/nwlistop/test_eaf.py ... -v`, then all tests pass
- [ ] Given `ruff check inewave/nwlistop/`, when I run it, then no errors on migrated files

## Implementation Guide

### Suggested Approach

The migration is mechanical. For each model file:

**Before** (`inewave/nwlistop/modelos/earmf.py`):

```python
from inewave.config import MESES_DF
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie

class EarmsAnos(ValoresSerie):
    __slots__ = []
    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [IntegerField(4, 2)]
        + [FloatField(8, 8 + 9 * i, 1) for i in range(len(MESES_DF))]
    )
```

**After:**

```python
from inewave.config import MESES_DF
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.tabular import ColumnDef
from inewave.nwlistop.modelos.blocos.tabela_serie_anual import (
    TabelaSerieAnual,
)

class EarmsAnos(TabelaSerieAnual):
    __slots__ = []
    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(8, 8 + 9 * i, 1))
        for i in range(len(MESES_DF))
    ]
```

Note: The `Line` import is no longer needed. The `HEADER_LINE` and `DATA_LINE` are replaced by `COLUMNS`. The `YEAR_LINE` is inherited from `TabelaSerieAnual` (default: `Line([IntegerField(4, 10)])`).

Process each file systematically. Use a checklist to track progress.

### Key Files to Modify

35 model files in `inewave/nwlistop/modelos/` and 35 handler files in `inewave/nwlistop/`.

### Patterns to Follow

- Extract field definitions from `DATA_LINE` and convert to `ColumnDef` list
- First ColumnDef is always "serie" (IntegerField)
- Remaining 12 ColumnDefs are the month columns (FloatField) using `MESES_DF` names
- Some files have different FloatField sizes/precisions -- preserve them exactly

### Pitfalls to Avoid

- Different model files use different `FloatField` sizes and precisions -- do NOT standardize them; preserve the exact field definitions
- Some models have additional columns beyond the standard 13 -- read each file carefully
- Do NOT modify the handler file's public interface or properties
- Run the specific test after each file migration to catch issues early

## Testing Requirements

### Unit Tests

Run each file's existing test after migration. No new tests needed for this batch.

### Integration Tests

Run `pytest tests/nwlistop/ -x` after the full batch.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-004, ticket-006
- **Blocks**: ticket-013

## Effort Estimate

**Points**: 3
**Confidence**: High (mechanical, repetitive)
