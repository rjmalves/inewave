# ticket-010 Batch migrate ArquivoSubmercadoPatamar and ArquivoREEPatamar model files (47 files)

## Context

### Background

With `TabelaSeriePatamarAnual` created (ticket-005) and patamar archive base classes updated (ticket-007), the patamar model files can be migrated. This ticket covers the two largest patamar groups: ArquivoSubmercadoPatamar (35 subclasses) and ArquivoREEPatamar (12 subclasses).

### Relation to Epic

This is the first patamar batch migration, covering 47 of the ~87 patamar model files.

### Current State

**ArquivoSubmercadoPatamar subclasses (35 model files):**
cmarg, cmargmed, cterm, cdef, deficit, exces, mercl, gttot, ghtotm, ghmaxm, ghmaxmr, ghidrm, eafm, eafbm, earmfm, earmfpm, edesvcm, evertm, evapom, perdfm, corteolm, dlppdfmaxm, dlpptbmaxm, vmortm, verturbm, mevminm, vevminm, viol_lpp_dfmaxm, viol_lpp_tbmaxm, viol_ghminm, viol_evminm, vghminm, invadem, geolm, fteolm

**ArquivoREEPatamar subclasses (12 model files):**
ghidr, ghtot, ghmax, ghmaxr, dlppdfmax, dlpptbmax, viol_lpp_dfmax, viol_lpp_tbmax, viol_ghmin, vghmin, rhslppdf, rhslpptb

All 47 use `ValoresSeriePatamar` subclasses with the standard `[serie, patamar] + [12 months]` DATA_LINE pattern.

Note: `cmarg.py` and `cmargmed.py` have VERSIONS with multiple block classes (e.g., `CmargsAnos27` and `CmargsAnos`). Both version variants must be migrated.

## Specification

### Requirements

1. Convert each model file's block class(es) from `ValoresSeriePatamar` subclass to `TabelaSeriePatamarAnual` subclass
2. Replace `HEADER_LINE` / `DATA_LINE` with `COLUMNS`
3. Update handler files' `BLOCKS` and `VERSIONS` lists
4. Run tests for each migrated file

### Inputs/Props

Mechanical transformation: `DATA_LINE` fields become `ColumnDef` list with "serie" first, "patamar" second, then 12 month columns.

### Outputs/Behavior

All 47 model files use `TabelaSeriePatamarAnual` with `COLUMNS`. All tests pass.

### Error Handling

No behavioral changes.

## Acceptance Criteria

- [ ] Given all 47 model files, when I read them, then each uses `TabelaSeriePatamarAnual` with `COLUMNS`
- [ ] Given `cmarg.py` and `cmargmed.py`, when I read them, then both VERSIONS variant classes are migrated
- [ ] Given `pytest tests/nwlistop/test_cmarg.py tests/nwlistop/test_deficit.py tests/nwlistop/test_ghidr.py ... -v`, when I run it, then all tests pass

## Implementation Guide

### Suggested Approach

Same mechanical process as tickets 008-009, but with the patamar column convention:

**Before:**

```python
class CmargsAnos(ValoresSeriePatamar):
    __slots__ = []
    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [IntegerField(4, 2), IntegerField(2, 9)]
        + [FloatField(11, 14 + 11 * i, 2) for i in range(len(MESES_DF))]
    )
```

**After:**

```python
class CmargsAnos(TabelaSeriePatamarAnual):
    __slots__ = []
    COLUMNS = [
        ColumnDef("serie", IntegerField(4, 2)),
        ColumnDef("patamar", IntegerField(2, 9)),
    ] + [
        ColumnDef(MESES_DF[i], FloatField(11, 14 + 11 * i, 2))
        for i in range(len(MESES_DF))
    ]
```

### Key Files to Modify

47 model files in `inewave/nwlistop/modelos/` and 47 handler files in `inewave/nwlistop/`.

### Patterns to Follow

Same as ticket-008 but with patamar column as second ColumnDef.

### Pitfalls to Avoid

- Some files use `LiteralField` for patamar instead of `IntegerField` -- preserve the original field type
- `cmarg.py` and `cmargmed.py` have VERSIONS -- migrate all variant classes
- FloatField sizes and precisions vary across files -- preserve exactly

## Testing Requirements

### Unit Tests

Run each file's existing test after migration.

### Integration Tests

Run `pytest tests/nwlistop/ -x` after the full batch.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-005, ticket-007
- **Blocks**: ticket-013

## Effort Estimate

**Points**: 3
**Confidence**: High (mechanical, repetitive)
