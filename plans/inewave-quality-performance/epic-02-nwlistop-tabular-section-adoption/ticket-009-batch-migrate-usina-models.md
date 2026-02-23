# ticket-009 Batch migrate ArquivoUsina model files to TabelaSerieAnual (17 files)

## Context

### Background

With the `TabelaSerieAnual` base class (ticket-004) and archive base class updates (ticket-006) in place, this ticket migrates the 17 `ArquivoUsina` model files. These files follow the same `ValoresSerie` pattern as the REE/SIN files (ticket-008) but are associated with individual hydroelectric plants (usinas).

### Relation to Epic

This is the second batch migration ticket, completing the ValoresSerie-side migrations.

### Current State

17 model files in `inewave/nwlistop/modelos/` that subclass `ValoresSerie` and are used by `ArquivoUsina` handler files:

1. `desvuh.py`, 2. `vretiradauh.py`, 3. `qafluh.py`, 4. `dnegevap.py`,
2. `dposevap.py`, 6. `viol_pos_vretiruh.py`, 7. `pivarmincr.py`, 8. `pivarm.py`,
3. `viol_pos_evap.py`, 10. `vevapuh.py`, 11. `viol_neg_vretiruh.py`, 12. `vento.py`,
4. `viol_neg_evap.py`, 14. `varmuh.py`, 15. `varmpuh.py`, 16. `qincruh.py`,
5. `hmont.py`

Note: `pivarm.py` and `pivarmincr.py` have multiple ValoresSerie subclasses (2 each) due to VERSIONS support. These files also already have `VERSIONS` dictionaries. Preserve the VERSIONS structure.

## Specification

### Requirements

1. Convert each model file's block class(es) from `ValoresSerie` subclass to `TabelaSerieAnual` subclass
2. Replace `HEADER_LINE` / `DATA_LINE` with `COLUMNS`
3. Update handler files' `BLOCKS` lists
4. For files with VERSIONS (`pivarm`, `pivarmincr`): migrate both version variant classes
5. Run each file's test

### Inputs/Props

Same mechanical transformation as ticket-008.

### Outputs/Behavior

All 17 model files use `TabelaSerieAnual` with `COLUMNS`. All tests pass.

### Error Handling

No behavioral changes.

## Acceptance Criteria

- [ ] Given all 17 model files, when I read them, then each uses `TabelaSerieAnual` with `COLUMNS`
- [ ] Given `pivarm.py` and `pivarmincr.py`, when I read them, then both version variant classes are migrated and the `VERSIONS` dict on the handler is preserved
- [ ] Given `pytest tests/nwlistop/test_desvuh.py tests/nwlistop/test_varmuh.py ... -v`, when I run it, then all tests pass

## Implementation Guide

### Suggested Approach

Same mechanical process as ticket-008. Apply the transformation to each file.

Special attention for `pivarm.py` and `pivarmincr.py`:

- These have 2 ValoresSerie subclasses each (one per version)
- Both subclasses must be migrated to TabelaSerieAnual
- The handler file's VERSIONS dict references these classes -- update the references

### Key Files to Modify

17 model files in `/home/rogerio/git/inewave/inewave/nwlistop/modelos/` and 17 handler files in `/home/rogerio/git/inewave/inewave/nwlistop/`.

### Patterns to Follow

Same as ticket-008.

### Pitfalls to Avoid

- `pivarm` and `pivarmincr` have VERSIONS -- do not break the version dispatch
- `hmont.py` may have a unique field layout -- verify before applying the standard transformation

## Testing Requirements

### Unit Tests

Run each file's existing test after migration.

### Integration Tests

Run `pytest tests/nwlistop/ -x` after the full batch.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-004, ticket-006
- **Blocks**: ticket-013

## Effort Estimate

**Points**: 2
**Confidence**: High
