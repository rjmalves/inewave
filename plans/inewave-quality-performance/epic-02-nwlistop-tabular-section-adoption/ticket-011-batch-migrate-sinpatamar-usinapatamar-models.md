# ticket-011 Batch migrate ArquivoSINPatamar and ArquivoUsinaPatamar model files (47 files)

## Context

### Background

This ticket continues the patamar migration, covering the ArquivoSINPatamar (22 subclasses) and ArquivoUsinaPatamar (25 subclasses) model files.

### Relation to Epic

This is the second patamar batch migration, covering the remaining large groups.

### Current State

**ArquivoSINPatamar subclasses (22 model files):**
ghidrsin, ghtotsin, ghmaxsin, ghmaxrsin, gttotsin, dlppdfmaxs, dlpptbmaxs, defsin, excessin, deletricas, celetricas, cbombsin, geolsin, fteolsin, viol_lpp_dfmaxsin, viol_lpp_tbmaxsin, viol_ghminsin, viol_eletricasin, cviol_eletricasin, cviol_rhq_sin, vghminsin, c_v_rhq_s, c_v_rhv_s

**ArquivoUsinaPatamar subclasses (25 model files):**
ghiduh, vturuh, ghmax_fpha, ghmax_fphc, gh_fphexat, dfphauh, depminuh, qturuh, qvertuh, qdesviouh, vertuh, vdesviouh, hliq, hjus, dtbmax, dtbmin, dvazmax, geol, viol_turbmax, viol_turbmin, viol_vazmax, viol_vazmin, viol_fpha, viol_ghminuh, vghminuh

All use `ValoresSeriePatamar` subclasses.

## Specification

### Requirements

1. Convert all 47 model files from `ValoresSeriePatamar` to `TabelaSeriePatamarAnual`
2. Replace `HEADER_LINE` / `DATA_LINE` with `COLUMNS`
3. Update handler files' `BLOCKS` lists
4. Run tests for each migrated file

### Inputs/Props

Same mechanical transformation as ticket-010.

### Outputs/Behavior

All 47 model files use `TabelaSeriePatamarAnual` with `COLUMNS`. All tests pass.

### Error Handling

No behavioral changes.

## Acceptance Criteria

- [ ] Given all 47 model files, when I read them, then each uses `TabelaSeriePatamarAnual` with `COLUMNS`
- [ ] Given `pytest tests/nwlistop/test_ghiduh.py tests/nwlistop/test_defsin.py ... -v`, when I run it, then all tests pass

## Implementation Guide

### Suggested Approach

Same mechanical process as ticket-010. Special attention:

- ArquivoUsinaPatamar files may use `LiteralField` for patamar names
- Some usina files have non-standard column layouts -- read each DATA_LINE carefully before transforming

### Key Files to Modify

47 model files in `inewave/nwlistop/modelos/` and 47 handler files in `inewave/nwlistop/`.

### Patterns to Follow

Same as ticket-010.

### Pitfalls to Avoid

- Same as ticket-010: preserve field types, sizes, and precisions exactly
- Some UsinaPatamar files may have extra columns or different patamar field types

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
