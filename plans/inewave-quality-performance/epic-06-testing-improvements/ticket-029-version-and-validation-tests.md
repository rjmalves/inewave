# ticket-029 Add version-aware and validation tests

## Context

### Background

Epic 03 (Schema Versioning) established the version-aware read API (`read(version=...)`) and the validation API (`validate(version=...)`) for all handlers with `VERSIONS` dictionaries. Ticket-018 wrote the initial version-aware and validation tests, which now live in `tests/nwlistop/test_version_validate.py`. The current test file covers 3 of the 5 versioned handlers: Cmarg (correct + mismatch), Pivarm (correct + mismatch), and AvlCortesFpha (correct v28, mismatch v28->v28.16, correct v28.16, mismatch v28.16->v28). That is 8 total tests.

Two versioned handlers are NOT yet covered by version/validation tests: **Cmargmed** and **Pivarmincr**. Additionally, the existing per-handler test files (`test_cmarg.py`, `test_cmargmed.py`, `test_pivarm.py`, `test_pivarmincr.py`) have version-specific read tests (they call `read(version="27")` etc.) but lack explicit `validate()` calls. The newave `test_avl_cortesfpha_nwv.py` has version read tests but no validation tests (those live in `test_version_validate.py`).

### Relation to Epic

This ticket targets the second goal of Epic 06: "Add version-aware tests exercising `read(version=...)` API" and "Add validation tests exercising `validate()` API." It completes the coverage for all 5 versioned handlers.

### Current State

**Versioned handlers in the codebase** (from `plans/inewave-quality-performance/version-catalog.md`):

| Handler         | Version Keys        | Mock Data Available                              | Version Tests                      | Validate Tests                   |
| --------------- | ------------------- | ------------------------------------------------ | ---------------------------------- | -------------------------------- |
| `Cmarg`         | `"27"`, `"29.4.1"`  | `MockCmarg27`, `MockCmarg`                       | Yes (`test_cmarg.py`)              | Yes (`test_version_validate.py`) |
| `Cmargmed`      | `"28"`, `"29.4.1"`  | `MockCmargmed28`, `MockCmargmed`                 | Yes (`test_cmargmed.py`)           | **NO**                           |
| `Pivarm`        | `"28.12"`, `"29.2"` | `MockPivarm`, `MockPivarm_v29_2`                 | Yes (`test_pivarm.py`)             | Yes (`test_version_validate.py`) |
| `Pivarmincr`    | `"28.12"`, `"29.2"` | `MockPivarmincr`, `MockPivarmincr_v29_2`         | Yes (`test_pivarmincr.py`)         | **NO**                           |
| `AvlCortesFpha` | `"28"`, `"28.16"`   | `MockAvlCortesFphaNwv28`, `MockAvlCortesFphaNwv` | Yes (`test_avl_cortesfpha_nwv.py`) | Yes (`test_version_validate.py`) |

**Existing test patterns in `tests/nwlistop/test_version_validate.py`:**

```python
def test_validate_cmarg_correct_version():
    m: MagicMock = mock_open(read_data="".join(MockCmarg27))
    with patch("builtins.open", m):
        n = Cmarg.read(ARQ_TESTE, version="27")
    result: VersionMatchResult = n.validate(version="27")
    assert isinstance(result, VersionMatchResult)
    assert result.missing_types == []
    assert result.unexpected_types == []
    assert Submercado in result.found_types
    assert CmargsAnos27 in result.found_types

def test_validate_cmarg_mismatch_version():
    m: MagicMock = mock_open(read_data="".join(MockCmarg27))
    with patch("builtins.open", m):
        n = Cmarg.read(ARQ_TESTE, version="27")
    result: VersionMatchResult = n.validate(version="29.4.1")
    assert isinstance(result, VersionMatchResult)
    assert CmargsAnos in result.missing_types
    assert CmargsAnos27 in result.unexpected_types
```

## Specification

### Requirements

1. Add validation tests for **Cmargmed** (correct + mismatch) to `tests/nwlistop/test_version_validate.py`.
2. Add validation tests for **Pivarmincr** (correct + mismatch) to `tests/nwlistop/test_version_validate.py`.
3. Verify that the existing 8 validation tests still pass (no regressions from prior epics).
4. All new tests follow the exact pattern established in the existing `test_version_validate.py`.

### Inputs/Props

- **Cmargmed**: `MockCmargmed28` (older version data) and `MockCmargmed` (latest version data), from `tests/mocks/arquivos/cmargmed.py`.
  - Version `"28"`: Uses `CmargsAnos28` block class (from `inewave/nwlistop/modelos/cmargmed.py`)
  - Version `"29.4.1"` (default): Uses `CmargsAnos` block class
  - Header block: `REE` (from `inewave/nwlistop/modelos/blocos/ree.py`)

- **Pivarmincr**: `MockPivarmincr` (older version data) and `MockPivarmincr_v29_2` (latest version data), from `tests/mocks/arquivos/pivarmincr.py`.
  - Version `"28.12"`: Uses `PivarmincrAnos` block class (from `inewave/nwlistop/modelos/pivarmincr.py`)
  - Version `"29.2"` (default): Uses `PivarmincrAnos_v29_2` block class
  - Header block: `Usina` (from `inewave/nwlistop/modelos/blocos/usina.py`)

### Outputs/Behavior

- Correct version tests: `result.missing_types == []` and `result.unexpected_types == []`, with expected block types in `result.found_types`.
- Mismatch version tests: The expected block type for the requested version appears in `result.missing_types`, and the actual block type appears in `result.unexpected_types`.

### Error Handling

- If `validate()` is not available on the handler, the test will raise `AttributeError` -- this would indicate a regression in cfinterface integration.
- If block type names have changed, the import will fail at module level.

## Acceptance Criteria

- [ ] Given `Cmargmed` read with `version="28"`, when `validate(version="28")` is called, then `result.missing_types == []` and `result.unexpected_types == []` and `CmargsAnos28 in result.found_types`
- [ ] Given `Cmargmed` read with `version="28"`, when `validate(version="29.4.1")` is called, then `CmargsAnos in result.missing_types` and `CmargsAnos28 in result.unexpected_types`
- [ ] Given `Pivarmincr` read with `version="28.12"`, when `validate(version="28.12")` is called, then `result.missing_types == []` and `result.unexpected_types == []` and `PivarmincrAnos in result.found_types`
- [ ] Given `Pivarmincr` read with `version="28.12"`, when `validate(version="29.2")` is called, then `PivarmincrAnos_v29_2 in result.missing_types` and `PivarmincrAnos in result.unexpected_types`
- [ ] Given all new tests are added, when `pytest tests/nwlistop/test_version_validate.py -v` is run, then all 12 tests pass (8 existing + 4 new)
- [ ] Given the full test suite, when `pytest tests/ -v` is run, then the test count increases by 4

## Implementation Guide

### Suggested Approach

1. **Read the existing `test_version_validate.py`** to understand the imports and pattern.

2. **Add Cmargmed imports** at the top of the file:

   ```python
   from inewave.nwlistop.cmargmed import Cmargmed
   from inewave.nwlistop.modelos.cmargmed import CmargsAnos28, CmargsAnos
   from inewave.nwlistop.modelos.blocos.ree import REE
   from tests.mocks.arquivos.cmargmed import MockCmargmed28
   ```

   Note: `REE` and `CmargsAnos` may already be imported. Check existing imports before adding.

3. **Add Pivarmincr imports**:

   ```python
   from inewave.nwlistop.pivarmincr import Pivarmincr
   from inewave.nwlistop.modelos.pivarmincr import PivarmincrAnos, PivarmincrAnos_v29_2
   from tests.mocks.arquivos.pivarmincr import MockPivarmincr
   ```

   Note: `Usina` is already imported for Pivarm tests.

4. **Add 4 test functions** following the exact pattern. For Cmargmed:

   ```python
   def test_validate_cmargmed_correct_version():
       m: MagicMock = mock_open(read_data="".join(MockCmargmed28))
       with patch("builtins.open", m):
           n = Cmargmed.read(ARQ_TESTE, version="28")
       result: VersionMatchResult = n.validate(version="28")
       assert isinstance(result, VersionMatchResult)
       assert result.missing_types == []
       assert result.unexpected_types == []
       assert REE in result.found_types
       assert CmargsAnos28 in result.found_types

   def test_validate_cmargmed_mismatch_version():
       m: MagicMock = mock_open(read_data="".join(MockCmargmed28))
       with patch("builtins.open", m):
           n = Cmargmed.read(ARQ_TESTE, version="28")
       result: VersionMatchResult = n.validate(version="29.4.1")
       assert isinstance(result, VersionMatchResult)
       assert CmargsAnos in result.missing_types
       assert CmargsAnos28 in result.unexpected_types
   ```

5. **Verify mock data exists** by checking `tests/mocks/arquivos/cmargmed.py` for `MockCmargmed28` and `tests/mocks/arquivos/pivarmincr.py` for `MockPivarmincr`.

6. **Run tests**: `pytest tests/nwlistop/test_version_validate.py -v`

### Key Files to Modify

- `tests/nwlistop/test_version_validate.py` -- add 4 new test functions and necessary imports

### Key Files to Read (for reference)

- `inewave/nwlistop/cmargmed.py` -- handler with VERSIONS dict
- `inewave/nwlistop/modelos/cmargmed.py` -- model file with `CmargsAnos28` and `CmargsAnos`
- `inewave/nwlistop/pivarmincr.py` -- handler with VERSIONS dict
- `inewave/nwlistop/modelos/pivarmincr.py` -- model file with `PivarmincrAnos` and `PivarmincrAnos_v29_2`
- `tests/mocks/arquivos/cmargmed.py` -- mock data for Cmargmed
- `tests/mocks/arquivos/pivarmincr.py` -- mock data for Pivarmincr

### Patterns to Follow

- Follow the exact test structure in `tests/nwlistop/test_version_validate.py` lines 38-65 (Cmarg tests).
- Import `VersionMatchResult` from `cfinterface.versioning`.
- Test naming: `test_validate_{handler}_correct_version` and `test_validate_{handler}_mismatch_version`.
- Each test first reads with a specific version, then validates against correct or incorrect version.

### Pitfalls to Avoid

- **Check the exact mock variable names** -- `MockCmargmed28` (not `MockCmargmed_28` or `MockCmargmed_v28`). Read the import at the top of `tests/nwlistop/test_cmargmed.py` to confirm.
- **Check the exact block class names** in the model files -- `CmargsAnos28` vs `CmargsAnos` for cmargmed; `PivarmincrAnos` vs `PivarmincrAnos_v29_2` for pivarmincr.
- **The header block type differs between handlers** -- Cmargmed uses `REE`, Pivarmincr uses `Usina`. Use the correct header block in `result.found_types` assertions.
- **Do NOT modify existing tests** -- only add new tests at the end of the file.

## Testing Requirements

### Unit Tests

Each new validation test function IS a unit test. 4 new test functions total.

### Integration Tests

Not applicable -- this ticket adds tests, not production code.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: None (all prior epics are completed)
- **Blocks**: None

## Effort Estimate

**Points**: 1
**Confidence**: High
