# ticket-018 Write version-aware tests for versioned file classes

## Context

### Background

After tickets 014-017, the inewave library has `VERSIONS` dictionaries on all file handlers with known format differences between NEWAVE versions. The `read(version=...)` API resolves version-specific component lists, and the inherited `validate()` method checks parsed data against expected types. What remains is comprehensive test coverage for these version-aware code paths.

The existing test suite (1126+ tests) covers the default (latest) format of each file handler. Tests for older versions exist only for the 5 files that had VERSIONS before this epic: `cmarg`, `cmargmed`, `pivarm`, `pivarmincr`, and `avl_cortesfpha_nwv`. These existing version tests use the deprecated `set_version()` API.

This ticket adds tests for:

1. The `read(version=...)` API on all newly versioned handlers (using the modern API, not `set_version()`)
2. The `validate(version=...)` API on representative handlers
3. Migration of existing version tests from `set_version()` to `read(version=...)`

### Relation to Epic

This is the final ticket in Epic 03, ensuring that all version-aware code paths are tested. It depends on all prior tickets being complete.

### Current State

Existing version-aware tests (using deprecated `set_version()` API):

- `tests/nwlistop/test_cmarg.py`: Tests `set_version("27")` and `set_version("latest")` with `MockCmarg27` and `MockCmarg` mock data
- `tests/nwlistop/test_cmargmed.py`: Tests `set_version("28")` and `set_version("latest")` with `MockCmargmed28` and `MockCmargmed`
- `tests/nwlistop/test_pivarm.py`: Tests `set_version("28.12")` and `set_version("29.2")` with `MockPivarm` and `MockPivarm_v29_2`
- `tests/nwlistop/test_pivarmincr.py`: Tests `set_version("28.12")` and `set_version("29.2")` with `MockPivarmincr` and `MockPivarmincr_v29_2`
- `tests/newave/test_avl_cortesfpha_nwv.py`: Tests `set_version("28")` and `set_version("28.16")` with version-specific mocks

Mock data files are in `tests/mocks/arquivos/` (e.g., `cmarg.py`, `cmargmed.py`, `pivarm.py`, `pivarmincr.py`, `avl_cortesfpha_nwv.py`).

Test pattern: `mock_open(read_data="".join(MockData))` followed by `patch("builtins.open", m)` then `Handler.read(ARQ_TESTE)`.

## Specification

### Requirements

1. **Migrate existing version tests** to use `read(path, version=...)` instead of `set_version()`:
   - Replace `Cmarg.set_version("27"); n = Cmarg.read(path)` with `n = Cmarg.read(path, version="27")`
   - Replace `Cmarg.set_version("latest"); n = Cmarg.read(path)` with `n = Cmarg.read(path)` (no version = latest)
   - Apply to all 5 existing versioned test files
2. **Add version tests for all newly versioned handlers** from tickets 015-016:
   - For each handler that received VERSIONS, add at least one test per version key
   - Each test must read a mock data file with the appropriate version's format and verify the parsed data
3. **Add validate() tests** for at least 3 representative handlers (one nwlistop patamar, one nwlistop non-patamar, one newave if applicable):
   - Test `validate(version=correct_key)` returns `matched=True`
   - Test `validate(version=wrong_key)` returns `matched=False` or has non-empty `missing_types`
4. **Create mock data files** for new version-format combinations where they do not already exist
5. **Follow existing test conventions**: test file in `tests/nwlistop/` or `tests/newave/`, mock data in `tests/mocks/arquivos/`

### Inputs/Props

- Version catalog at `plans/inewave-quality-performance/version-catalog.md` (lists all versioned handlers and their version keys)
- All handler files with VERSIONS (from tickets 015-016)
- Existing test files and mock data files as templates
- cfinterface `VersionMatchResult` type for validate() assertions

### Outputs/Behavior

**Migrated test pattern** (replaces `set_version()`):

```python
# Before (deprecated):
def test_atributos_encontrados_cmarg27():
    m: MagicMock = mock_open(read_data="".join(MockCmarg27))
    with patch("builtins.open", m):
        Cmarg.set_version("27")
        n = Cmarg.read(ARQ_TESTE)
        assert n.valores is not None

# After (modern):
def test_atributos_encontrados_cmarg27():
    m: MagicMock = mock_open(read_data="".join(MockCmarg27))
    with patch("builtins.open", m):
        n = Cmarg.read(ARQ_TESTE, version="27")
        assert n.valores is not None
```

**New version test pattern**:

```python
def test_read_version_earmf_v27():
    """Read earmf with v27 format (narrower float fields)."""
    m: MagicMock = mock_open(read_data="".join(MockEarmf27))
    with patch("builtins.open", m):
        n = Earmf.read(ARQ_TESTE, version="27")
        assert n.valores is not None
        assert n.ree is not None
```

**Validate test pattern**:

```python
def test_validate_cmarg_version_match():
    """Validate returns matched=True when version matches."""
    m: MagicMock = mock_open(read_data="".join(MockCmarg27))
    with patch("builtins.open", m):
        n = Cmarg.read(ARQ_TESTE, version="27")
        result = n.validate(version="27")
        assert result.matched is True
        assert result.missing_types == []


def test_validate_cmarg_version_mismatch():
    """Validate detects mismatch when wrong version is specified."""
    m: MagicMock = mock_open(read_data="".join(MockCmarg27))
    with patch("builtins.open", m):
        n = Cmarg.read(ARQ_TESTE, version="27")
        result = n.validate(version="29.4.1")
        # The file was read with v27 blocks, so v29.4.1 types may be missing
        # or the default_ratio may be high
        assert not result.matched or len(result.missing_types) > 0
```

### Error Handling

- Tests should verify that reading with a version key older than all defined keys falls back gracefully (cfinterface emits a warning and uses default BLOCKS).
- Tests should verify that `validate()` on an empty file returns `matched=False` with `default_ratio=1.0`.

## Acceptance Criteria

- [ ] Given the existing 5 versioned test files, when inspecting them, then all calls to `set_version()` have been replaced with `read(path, version=...)`.
- [ ] Given each newly versioned handler from tickets 015-016, when inspecting the test directory, then there is at least one test that calls `Handler.read(path, version="<key>")` and asserts on parsed data.
- [ ] Given at least 3 versioned handlers, when inspecting their test files, then there are `validate()` tests that check both correct-version (`matched=True`) and wrong-version (`matched=False` or `missing_types` non-empty) scenarios.
- [ ] Given all new mock data files created, when inspecting them, then they follow the existing naming convention (`MockFoo`, `MockFoo27`, `MockFoo_v29_2`) and are placed in `tests/mocks/arquivos/`.
- [ ] Given the complete test suite including new tests, when running `pytest`, then all tests pass (1126+ original tests plus new tests).
- [ ] Given the `set_version()` migration, when searching the test directory for `set_version`, then zero occurrences remain.

## Implementation Guide

### Suggested Approach

1. **Migrate the 5 existing versioned test files first** (low risk, high value):
   - `tests/nwlistop/test_cmarg.py`: Replace `Cmarg.set_version("27")` + `Cmarg.read(path)` with `Cmarg.read(path, version="27")`. Replace `Cmarg.set_version("latest")` + `Cmarg.read(path)` with `Cmarg.read(path)`.
   - `tests/nwlistop/test_cmargmed.py`: Same pattern.
   - `tests/nwlistop/test_pivarm.py`: Same pattern.
   - `tests/nwlistop/test_pivarmincr.py`: Same pattern.
   - `tests/newave/test_avl_cortesfpha_nwv.py`: Same pattern.
   - Run `pytest` to verify no regressions.

2. **Read the version catalog** to get the list of all newly versioned handlers and their version keys.

3. **For each newly versioned handler**, create mock data and tests:
   a. Create a mock data file in `tests/mocks/arquivos/` with representative data in the older format. The mock should be a list of strings (lines), following the convention of existing mocks (e.g., `MockCmarg27` in `tests/mocks/arquivos/cmarg.py`).
   b. Add a test function in the corresponding test file (e.g., `tests/nwlistop/test_earmf.py`) that reads with `version=...` and asserts on parsed data.
   c. If the test file does not exist, create it following the existing pattern.

4. **Add validate() tests** for 3 representative handlers:
   - One nwlistop patamar handler (e.g., `Cmarg`)
   - One nwlistop non-patamar handler (e.g., `Pivarm` or `Earmf`)
   - One newave handler (if any received VERSIONS in ticket-015)
   - Place these in the existing test files or in a new `tests/nwlistop/test_version_validate.py`.

5. **Verify zero `set_version` calls remain** in the test directory:

   ```bash
   grep -r "set_version" tests/
   ```

6. Run `pytest --tb=short` and `ruff check tests/`.

### Key Files to Modify

**Existing test files to migrate** (replace `set_version()` with `version=...`):

- `tests/nwlistop/test_cmarg.py`
- `tests/nwlistop/test_cmargmed.py`
- `tests/nwlistop/test_pivarm.py`
- `tests/nwlistop/test_pivarmincr.py`
- `tests/newave/test_avl_cortesfpha_nwv.py`

**Existing mock data files** (reference, may need additions):

- `tests/mocks/arquivos/cmarg.py` (has `MockCmarg27`, `MockCmarg`)
- `tests/mocks/arquivos/cmargmed.py` (has `MockCmargmed28`, `MockCmargmed`)
- `tests/mocks/arquivos/pivarm.py` (has `MockPivarm`, `MockPivarm_v29_2`)
- `tests/mocks/arquivos/pivarmincr.py` (has `MockPivarmincr`, `MockPivarmincr_v29_2`)
- `tests/mocks/arquivos/avl_cortesfpha_nwv.py` (has `MockAvlCortesFphaNwv28`, `MockAvlCortesFphaNwv`)

**New test files** (for newly versioned handlers, exact list from version catalog):

- Test files in `tests/nwlistop/` for each newly versioned nwlistop handler
- Test files in `tests/newave/` for each newly versioned newave handler
- New mock data files in `tests/mocks/arquivos/` for version-specific formats

### Patterns to Follow

- **Test function naming**: `test_atributos_encontrados_<handler>_v<version>()` or `test_read_version_<handler>_v<version>()`. Follow the existing convention in the file being modified.
- **Mock data naming**: `MockFoo` (latest), `MockFoo27` (v27), `MockFoo_v29_2` (v29.2). Follow the existing convention.
- **Test structure**: Each test function reads mock data via `mock_open()` and `patch("builtins.open", m)`, calls `Handler.read(path, version=...)`, and asserts on `.valores`, `.submercado`/`.usina`/`.ree`, and specific data values.
- **ARQ_TESTE**: Always `"./tests/mocks/arquivos/__init__.py"` -- a dummy path for the mock_open pattern.
- **Import VersionMatchResult** from cfinterface for validate tests:
  ```python
  from cfinterface.versioning import VersionMatchResult
  ```

### Pitfalls to Avoid

- **`set_version()` mutates the class-level BLOCKS** -- after calling `set_version("27")`, subsequent `read()` calls without `set_version()` would still use v27 blocks. The new `read(version=...)` API does NOT mutate the class. This means test ordering issues related to `set_version()` are eliminated by this migration.
- **Mock data must match the version's field layout exactly** -- if v27 uses `FloatField(8, ...)` then mock data lines must have 8-character-wide float fields, not 11-character-wide ones. Copy field widths from the model class COLUMNS definition.
- **Do not delete mock data files for old versions** -- they may be used by downstream test suites.
- **validate() tests depend on how cfinterface counts types** -- read the `validate_version()` implementation carefully. With nwlistop files, the data container holds header blocks + data blocks. The `default_ratio` reflects how many items are `DefaultBlock`.

## Testing Requirements

### Unit Tests

This ticket IS the testing ticket. All tests must pass via `pytest`.

### Integration Tests

Not applicable (all tests use mock_open, not real files).

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-015, ticket-016, ticket-017
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Medium (effort depends on how many files received VERSIONS in tickets 015-016; mock data creation is the most time-consuming part)
