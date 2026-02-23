# ticket-013 Clean up deprecated block classes and run full verification

## Context

### Background

After all batch migrations (tickets 008-012), the old `ValoresSerie` and `ValoresSeriePatamar` block classes should no longer be imported by any model file. This ticket removes or deprecates them and runs a comprehensive verification of the entire nwlistop module.

### Relation to Epic

This is the closing ticket for Epic 02. It ensures the migration is complete and clean.

### Current State

After tickets 008-012:

- All model files use `TabelaSerieAnual` or `TabelaSeriePatamarAnual`
- The old block classes in `inewave/nwlistop/modelos/blocos/valoresserie.py` and `valoresseriepatamar.py` may still exist but should have zero importers

## Specification

### Requirements

1. Verify that no production code imports `ValoresSerie` or `ValoresSeriePatamar`
2. If zero importers: add deprecation warnings to the old classes (do not delete them yet, as external code might reference them)
3. Verify all 430+ tests pass
4. Verify `ruff check` and `mypy` are clean
5. Run a LOC comparison: count lines in `inewave/nwlistop/modelos/` before and after the migration
6. Update `__init__.py` files if needed

### Inputs/Props

The fully migrated codebase.

### Outputs/Behavior

- Old block classes have deprecation warnings
- All tests pass
- LOC reduction is documented
- No ruff or mypy errors

### Error Handling

If any production code still imports the old classes, trace the import chain and migrate or update it.

## Acceptance Criteria

- [ ] Given `grep -rn "from.*valoresserie import" inewave/`, when I run it, then only the deprecation-wrapper file (if any) is returned
- [ ] Given `grep -rn "from.*valoresseriepatamar import" inewave/`, when I run it, then only the deprecation-wrapper file (if any) is returned
- [ ] Given `pytest tests/ -x`, when I run it, then all tests pass (exit code 0)
- [ ] Given `ruff check inewave/`, when I run it, then zero errors
- [ ] Given `mypy inewave/`, when I run it, then no new errors

## Implementation Guide

### Suggested Approach

1. Run `grep -rn "from.*valoresserie import" inewave/` and `grep -rn "from.*valoresseriepatamar import" inewave/` to find remaining importers
2. For any remaining importers: migrate them (should only be archive base classes -- but those were updated in tickets 006-007)
3. Add deprecation warnings to old classes:
   ```python
   import warnings
   class ValoresSerie(Block):
       def __init__(self, *args, **kwargs):
           warnings.warn(
               "ValoresSerie is deprecated. Use TabelaSerieAnual.",
               DeprecationWarning,
               stacklevel=2,
           )
           super().__init__(*args, **kwargs)
   ```
4. Run full test suite
5. Count LOC: `find inewave/nwlistop/modelos -name "*.py" -exec cat {} \; | wc -l`

### Key Files to Modify

- `/home/rogerio/git/inewave/inewave/nwlistop/modelos/blocos/valoresserie.py` (add deprecation)
- `/home/rogerio/git/inewave/inewave/nwlistop/modelos/blocos/valoresseriepatamar.py` (add deprecation)
- Any remaining importers

### Patterns to Follow

- Use `warnings.warn(..., DeprecationWarning, stacklevel=2)` consistent with cfinterface conventions

### Pitfalls to Avoid

- Do NOT delete the old classes -- they may be imported by external packages
- Do NOT suppress the deprecation in tests -- let the warnings be visible

## Testing Requirements

### Unit Tests

Run full `pytest tests/ --cov=inewave`.

### Integration Tests

Verify coverage did not drop.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-008, ticket-009, ticket-010, ticket-011, ticket-012
- **Blocks**: All tickets in Epic 03+

## Effort Estimate

**Points**: 2
**Confidence**: High
