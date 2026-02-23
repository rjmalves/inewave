# ticket-003 Verify full test suite and fix regressions after StorageType migration

## Context

### Background

After bumping cfinterface to >= 1.9.0 (ticket-001) and migrating all 16 `STORAGE = "BINARY"` string literals to `StorageType.BINARY` (ticket-002), we need to verify that all 430+ existing tests pass, that ruff and mypy are clean, and that no deprecation warnings are emitted.

### Relation to Epic

This is the verification and cleanup ticket that closes Epic 01. It gates the transition to Epic 02.

### Current State

The codebase has been updated with:

- cfinterface >= 1.9.0 dependency (ticket-001)
- `StorageType.BINARY` in 16 newave files (ticket-002)
- No other changes to production code

## Specification

### Requirements

1. Run the full pytest suite (`pytest tests/ --cov=inewave`) and verify all tests pass
2. Run `ruff check inewave/` and verify zero errors
3. Run `mypy inewave/` and verify it passes (at current strictness level)
4. Run a quick smoke test that instantiates key file classes and verifies no `DeprecationWarning` is emitted
5. If any test fails, investigate and fix the root cause (the fix should be minimal and directly related to the cfinterface upgrade)

### Inputs/Props

- The codebase after ticket-001 and ticket-002 are complete

### Outputs/Behavior

- All tests pass
- ruff and mypy are clean
- No DeprecationWarning from StorageType usage

### Error Handling

If tests fail:

- Check if the failure is related to cfinterface API changes (unlikely since v1.9.0 is fully backward compatible)
- Check if the failure is a pre-existing issue unrelated to this migration
- Document any fixes made in the commit message

## Acceptance Criteria

- [ ] Given the full test suite, when I run `pytest tests/ -x`, then all tests pass (exit code 0)
- [ ] Given the inewave source, when I run `ruff check inewave/`, then zero errors are reported
- [ ] Given the inewave source, when I run `mypy inewave/`, then no new errors are introduced
- [ ] Given a Python session, when I run the following code, then zero DeprecationWarnings are captured:
  ```python
  import warnings
  with warnings.catch_warnings(record=True) as w:
      warnings.simplefilter("always")
      from inewave.newave.hidr import Hidr
      from inewave.newave.vazoes import Vazoes
      from inewave.newave.forward import Forward
      assert len([x for x in w if issubclass(x.category, DeprecationWarning)]) == 0
  ```

## Implementation Guide

### Suggested Approach

1. Run `uv run pytest tests/ --cov=inewave --cov-report=term-missing -x` and observe results
2. Run `uv run ruff check inewave/`
3. Run `uv run mypy inewave/`
4. If all pass, run the deprecation warning smoke test:
   ```python
   import warnings
   with warnings.catch_warnings(record=True) as w:
       warnings.simplefilter("always")
       # Import all 16 modified file classes
       from inewave.newave.cortes import Cortes
       from inewave.newave.cortesh import Cortesh
       from inewave.newave.hidr import Hidr
       # ... etc for all 16
   deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
   print(f"Deprecation warnings: {len(deprecation_warnings)}")
   for dw in deprecation_warnings:
       print(f"  {dw.filename}:{dw.lineno}: {dw.message}")
   ```
5. Fix any issues found

### Key Files to Modify

Ideally none -- this ticket is a verification gate. If fixes are needed, they will be in the 16 files modified in ticket-002 or in test files.

### Patterns to Follow

- Do NOT modify test files to make tests pass (the production code should be the one that is correct)
- If a test fails due to a genuine cfinterface behavioral change, adapt the production code to match

### Pitfalls to Avoid

- Do NOT skip failing tests
- Do NOT suppress warnings with `filterwarnings` in conftest.py
- Do NOT modify unrelated files

## Testing Requirements

### Unit Tests

This ticket IS the test verification. No new tests needed.

### Integration Tests

The full pytest suite serves as the integration test.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-002
- **Blocks**: All tickets in Epic 02

## Effort Estimate

**Points**: 1
**Confidence**: High
