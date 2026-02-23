# ticket-012 Batch migrate remaining archive types (Restricao, Bombeamento, ClasseTermica, PAR) (16 files)

## Context

### Background

This ticket covers the remaining nwlistop model files that were not handled in tickets 008-011. These are smaller, less common archive types.

### Relation to Epic

This completes the batch migration phase, covering the "long tail" of nwlistop file types.

### Current State

**ArquivoRestricao subclasses (4 files, ValoresSerie):**
viol_rhv, form_rhv (if applicable), viol_rhq, form_rhq (if applicable)

**ArquivoRestricaoPatamar subclasses (8 files, ValoresSeriePatamar):**
cviol_rhq, cviol_rhv, cviol_eletrica, c_v_rhq, c_v_rhv, viol_eletrica, viol_rhq, viol_rhv, intercambio, form_rhq, form_rhv

**ArquivoEstacaoBombeamentoPatamar subclasses (2 files):**
cbomb, qbomb, vbomb

**ArquivoClasseTermicaSubmercadoPatamar subclasses (1 file):**
gtert

**ArquivoPARSubmercadoPatamar subclasses (1 file):**
(if applicable)

Note: The exact file list must be verified against the codebase. Some files may already have been covered in earlier tickets if they use a different base class than expected.

## Specification

### Requirements

1. Migrate all remaining model files to `TabelaSerieAnual` or `TabelaSeriePatamarAnual`
2. Handle `gtert.py` specially -- it uses `ValoresClasseTermicaSeriePatamar` which has a different read pattern with additional thermal class grouping. If the pattern is too different from standard `TabelaSeriePatamarAnual`, create a specialized subclass or leave this single file on the old pattern.
3. Run all tests

### Inputs/Props

Same mechanical transformation, with exceptions noted above.

### Outputs/Behavior

All remaining model files migrated (or explicitly excluded with documented reason). All tests pass.

### Error Handling

If `gtert.py`'s `ValoresClasseTermicaSeriePatamar` pattern is too different, document why and leave it unmigrated.

## Acceptance Criteria

- [ ] Given all remaining model files, when I read them, then each is migrated or has a documented exclusion reason
- [ ] Given `pytest tests/nwlistop/ -x`, when I run it, then all tests pass
- [ ] Given `ruff check inewave/nwlistop/`, when I run it, then no errors

## Implementation Guide

### Suggested Approach

1. List all nwlistop model files not yet migrated
2. For each file, determine which base class it uses
3. Apply the standard transformation for ValoresSerie or ValoresSeriePatamar subclasses
4. For `gtert.py`: Read `ValoresClasseTermicaSeriePatamar` carefully. If it has the same `[serie, patamar, months]` structure, migrate. If it has additional columns (thermal class name, submercado), create a `TabelaClasseTermicaPatamarAnual` variant or leave unmigrated.

### Key Files to Modify

~16 model files + handler files in `inewave/nwlistop/`.

### Patterns to Follow

Same as tickets 008-011.

### Pitfalls to Avoid

- `gtert.py` may need special handling -- do not force it into the standard pattern if it does not fit
- Restricao files may have a different header block (Restricao instead of Submercado/REE/Usina) -- this affects the archive class but not the model class migration

## Testing Requirements

### Unit Tests

Run each file's existing test.

### Integration Tests

Run `pytest tests/nwlistop/ -x`.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-006, ticket-007
- **Blocks**: ticket-013

## Effort Estimate

**Points**: 2
**Confidence**: Medium (gtert.py may require special handling)
