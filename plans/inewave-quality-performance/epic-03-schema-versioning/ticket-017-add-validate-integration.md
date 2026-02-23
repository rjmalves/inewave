# ticket-017 Add validate() integration to versioned file classes

## Context

### Background

cfinterface 1.9.0 provides a `validate()` method on `BlockFile`, `SectionFile`, and `RegisterFile` that checks whether parsed data matches the expected component types for a given version. The method signature is:

```python
def validate(self, version: Optional[str] = None, threshold: float = 0.5) -> VersionMatchResult
```

It works as follows:

1. If `version` is provided and `VERSIONS` is non-empty, it calls `resolve_version(version, VERSIONS)` to get the expected component type list.
2. If `version` is `None` or `VERSIONS` is empty, it uses the default `BLOCKS`/`SECTIONS` list.
3. It then calls `validate_version(data, expected_types, default_type, threshold)` which iterates over parsed data items, classifies each by type, and returns a `VersionMatchResult` NamedTuple.

The `VersionMatchResult` contains: `matched` (bool), `expected_types`, `found_types`, `missing_types`, `unexpected_types`, and `default_ratio` (float -- ratio of items that are the default/fallback type). `matched` is True when no expected types are missing AND `default_ratio < threshold`.

This `validate()` method is **already inherited** by all inewave handler classes from cfinterface base classes. No implementation code needs to be written in inewave. This ticket is about:

1. Verifying that `validate()` works correctly with inewave's block/section types
2. Adding convenience documentation / examples
3. Optionally adding a thin wrapper or helper if the inherited API is insufficient

### Relation to Epic

This ticket bridges the VERSIONS implementation (tickets 015-016) with the testing ticket (018). It ensures the validate API works end-to-end before tests are written for it.

### Current State

- `validate()` is inherited from `BlockFile` (see `/home/rogerio/git/cfinterface/cfinterface/files/blockfile.py` lines 94-111) and `SectionFile` (see `/home/rogerio/git/cfinterface/cfinterface/files/sectionfile.py` lines 94-111).
- `validate_version()` in `/home/rogerio/git/cfinterface/cfinterface/versioning.py` lines 45-86 uses `type(item) is default_type` for exact type comparison, so subclasses of `DefaultBlock`/`DefaultSection` count as real components.
- The default types are `DefaultBlock` (for BlockFile) and `DefaultSection` (for SectionFile).
- No inewave code currently calls `validate()` -- this is a new API for downstream consumers.
- The `threshold` parameter defaults to 0.5, meaning validation fails if more than 50% of parsed items are the default/fallback type (indicating the file was not successfully parsed by the expected component types).

## Specification

### Requirements

1. **Verify `validate()` works** with all handler classes that have `VERSIONS` (from tickets 015-016). Specifically:
   - For nwlistop `BlockFile` handlers: call `validate(version="<key>")` on a parsed file and verify it returns `VersionMatchResult(matched=True, ...)` when the version is correct.
   - For newave `SectionFile` handlers: same verification.
   - For nwlistop `BlockFile` handlers: call `validate(version="<wrong_key>")` and verify `matched=False` or `missing_types` is non-empty.
2. **Document the validate() API** by adding a usage example in the epic-03 learnings or in a docstring on a representative handler class.
3. **Evaluate whether a convenience helper is needed**. Possible helpers:
   - A `detect_version()` method that tries all VERSIONS keys and returns the best-matching one
   - A `validate_or_warn()` method that logs a warning if validation fails
   - **Decision**: Only add a helper if the inherited `validate()` is insufficient for common use cases. If the inherited API is adequate, document it and move on.
4. **If a helper is added**, implement it as a mixin or on the archive base classes (ArquivoREE, ArquivoUsina, etc.) rather than on every individual handler class.

### Inputs/Props

- All handler files that received VERSIONS in tickets 015-016
- cfinterface `validate()` implementation (read-only reference)
- cfinterface `VersionMatchResult` and `validate_version()` (read-only reference)

### Outputs/Behavior

**Minimum output**: Verification that `validate()` works correctly with inewave types. This is captured in the verification script/tests.

**If a helper is added** (e.g., `detect_version()`), it would look like:

```python
# On an archive base class, e.g., ArquivoREE
@classmethod
def detect_version(cls, file_instance: "ArquivoREE") -> Optional[str]:
    """Try all VERSIONS keys and return the best-matching version key."""
    if not cls.VERSIONS:
        return None
    best_key = None
    best_ratio = 1.0
    for key in cls.VERSIONS:
        result = file_instance.validate(version=key)
        if result.matched and result.default_ratio < best_ratio:
            best_key = key
            best_ratio = result.default_ratio
    return best_key
```

**Decision on helper**: If the inherited `validate()` is sufficient for the test suite in ticket-018 and for documented use cases, no helper is needed. Document the decision either way.

### Error Handling

- `validate()` never raises exceptions -- it always returns a `VersionMatchResult`. No error handling needed.
- If `VERSIONS` is empty on a handler class, `validate(version="X")` falls back to the default component list. This is correct behavior.

## Acceptance Criteria

- [ ] Given a nwlistop handler with VERSIONS (e.g., `Cmarg`), when reading a v27-format file with `Cmarg.read(path, version="27")` and calling `.validate(version="27")`, then `result.matched` is `True` and `result.missing_types` is empty.
- [ ] Given a nwlistop handler with VERSIONS (e.g., `Cmarg`), when reading a v27-format file with `Cmarg.read(path, version="27")` and calling `.validate(version="29.4.1")`, then `result.matched` is `False` or `result.missing_types` contains the v29.4.1-specific type(s).
- [ ] Given a newave handler with VERSIONS, when reading a file and calling `.validate()` (no version), then validation runs against the default SECTIONS/BLOCKS list and returns a `VersionMatchResult`.
- [ ] Given the investigation of whether a `detect_version()` helper is needed, when reviewing the ticket output, then there is a documented decision with rationale for whether the helper was added or deferred.
- [ ] Given no behavioral changes to existing code paths, when running `pytest`, then the full test suite (1126+ tests) passes.

## Implementation Guide

### Suggested Approach

1. **Start with manual verification** using an interactive Python session or a small script:

   ```python
   from inewave.nwlistop.cmarg import Cmarg
   from unittest.mock import patch
   from tests.mocks.mock_open import mock_open
   from tests.mocks.arquivos.cmarg import MockCmarg27

   m = mock_open(read_data="".join(MockCmarg27))
   with patch("builtins.open", m):
       cf = Cmarg.read("test.dat", version="27")
       result = cf.validate(version="27")
       print(f"matched={result.matched}, missing={result.missing_types}, "
             f"default_ratio={result.default_ratio}")
   ```

2. **Test cross-version validation** (reading with one version, validating against another) to confirm mismatch detection.
3. **Evaluate the need for `detect_version()`**:
   - If downstream users commonly have files of unknown version, `detect_version()` is valuable.
   - If version is always known from context (e.g., the NEWAVE deck specifies the model version), the inherited `validate()` is sufficient.
   - Document the decision.
4. **If a helper is needed**, add it to the archive base classes in `inewave/nwlistop/modelos/arquivos/` as a mixin method. All 14 archive base classes could benefit.
5. Run the full test suite.

### Key Files to Modify

- Potentially: `inewave/nwlistop/modelos/arquivos/arquivoree.py`, `arquivousina.py`, `arquivosubmercado.py`, `arquivosubmercadopatamar.py` and other archive base classes -- only if a helper method is added.
- Verification script (temporary, can be deleted after verification).

### Patterns to Follow

- The `validate()` method is inherited from cfinterface and should NOT be overridden. Only add new methods (like `detect_version()`) if needed.
- If adding a helper, use `@classmethod` pattern consistent with the existing codebase.
- cfinterface's `validate_version()` uses `type(item) is default_type` (identity check), not `isinstance()`. This means `DefaultBlock` subclasses are NOT counted as defaults -- they are counted as real matched types. This is the correct behavior for inewave.

### Pitfalls to Avoid

- **Do not override `validate()`** on inewave handler classes. The inherited implementation is correct and tested.
- **Do not assume `validate()` checks data content** -- it only checks component type presence and ratios. A file could validate as the correct version structurally but have garbage data values.
- **The `threshold` parameter matters**: with the default 0.5, a file where >50% of items are `DefaultBlock` (unrecognized) will fail validation even if all expected types are found. This is intentional -- it catches files that are mostly unparsed.
- **`validate()` with no version and no VERSIONS dict** validates against the default BLOCKS/SECTIONS list. This is a baseline sanity check, not a version check.

## Testing Requirements

### Unit Tests

Verification of `validate()` behavior is the primary deliverable. If verification is done via pytest tests, they should go in `tests/nwlistop/test_validate.py` or similar. However, comprehensive version-aware tests are deferred to ticket-018.

### Integration Tests

Not applicable.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-015, ticket-016 (VERSIONS must be defined before validate can be verified)
- **Blocks**: ticket-018

## Effort Estimate

**Points**: 1
**Confidence**: High (the `validate()` implementation already exists in cfinterface; this is verification and optional helper work)
