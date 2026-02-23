# Learnings: Epic 01 - Foundation and StorageType Migration

## Metadata

- **Epic**: epic-01-foundation-and-storagetype-migration
- **Completed**: 2026-02-23
- **Tickets completed**: 3
- **Key files changed**: `pyproject.toml`, `inewave/__init__.py`, all 16 files under `inewave/newave/` with `STORAGE = "BINARY"`, `tests/libs/test_eolica.py`, `tests/libs/test_restricoes.py`, `/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py`

## Patterns Established

- **StorageType enum import pattern**: Each file that declares a binary storage class attribute now imports `from cfinterface.storage import StorageType` immediately after all other `cfinterface` imports and before any `inewave` imports, then declares `STORAGE = StorageType.BINARY` as the class attribute. The 16 migrated files in `inewave/newave/` (e.g., `inewave/newave/hidr.py`, `inewave/newave/vazoes.py`) are the canonical reference for this placement rule.

- **uv local source override**: When a dependency is not yet published to PyPI, the `[tool.uv.sources]` section in `pyproject.toml` overrides the resolution with a local path. The pattern is `cfinterface = { path = "/home/rogerio/git/cfinterface" }` in `pyproject.toml` while the `dependencies` array still declares the version-bounded form `"cfinterface>=1.9.0"`. This allows version-bounded declarations to remain accurate while local development proceeds before a PyPI release.

- **nwlistop/nwlistcf files do not carry STORAGE**: Only the 16 `newave/` files use an explicit `STORAGE` attribute. The `nwlistop` and `nwlistcf` modules inherit the default `StorageType.TEXT` from their `BlockFile` base class and must NOT be given an explicit `STORAGE = StorageType.TEXT` declaration, as this would be redundant noise.

## Architectural Decisions

- **Keep `>=` version bound, not `==` pin**: The dependency in `pyproject.toml` was updated to `"cfinterface>=1.9.0"` rather than `"cfinterface==1.9.0"`. The alternative (pinning to an exact version) was rejected because forward compatibility is more important than strict reproducibility at this layer -- inewave is a library, not an application.

- **Fix cfinterface bugs in the local copy rather than working around them in inewave**: When cfinterface 1.9.0 was found to have a bug in `_is_null()` that caused `TypeError` on `pandas.NaT` (because `math.isnan` raises `TypeError` on non-numeric types), the fix was applied directly to `/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py` rather than adding a workaround in inewave. The rationale: inewave should not paper over upstream bugs; fixing upstream keeps the fix in the right place and benefits all consumers of cfinterface.

- **Fix tests to use same-instance objects with identity-based remove()**: When cfinterface 1.9.0 changed `RegisterData._index_of()` from equality (`==`) to identity (`is`) lookup, the tests in `tests/libs/test_eolica.py` and `tests/libs/test_restricoes.py` needed to be updated. The tests were calling `cf2.data.remove(cf2.pee_cad()[0])` and `cf2.data.remove(cf2.re()[0])` -- these accessor methods return the same object reference that lives in the container, so the fix was already correct by construction. The issue was that cfinterface 1.8.0 allowed removing a register fetched from a different container instance (via equality), whereas 1.9.0 requires the exact object instance that lives in the container.

## Files & Structures Created

- `pyproject.toml`: Updated `dependencies` to `"cfinterface>=1.9.0"` and added `[tool.uv.sources]` with local path override. This file is the single source of truth for the dependency floor; future epics do not need to change it unless a newer cfinterface feature requires a higher bound.

- `inewave/__init__.py`: Version bumped to `"1.13.0"`. Hatchling reads this file for the package version via `[tool.hatch.version] path = "inewave/__init__.py"`.

- All 16 binary storage files in `inewave/newave/`: `cortes.py`, `cortesh.py`, `enavazb.py`, `enavazf.py`, `energiab.py`, `energiaf.py`, `energias.py`, `engnat.py`, `forward.py`, `forwarh.py`, `hidr.py`, `vazaob.py`, `vazaof.py`, `vazaos.py`, `vazinat.py`, `vazoes.py`. All now declare `STORAGE = StorageType.BINARY` with the proper import.

- `/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py`: New utility module added to cfinterface containing `_is_null()` with NaT-safe handling. This is in the local cfinterface copy, not in the inewave repository.

## Conventions Adopted

- **Import ordering for cfinterface + inewave files**: Third-party `cfinterface` imports come first (all on adjacent lines), then `inewave` local imports, then stdlib `typing` imports at the bottom of the import block. The `StorageType` import belongs in the cfinterface group, not as a standalone import after a blank line.

- **No suppression of DeprecationWarnings in conftest.py**: Warnings must be fixed at the source (by using the proper enum) rather than filtered at the test configuration level. No `filterwarnings` directives were added.

- **Test accessor methods return same-container objects**: Tests that call `cf.data.remove(cf.some_accessor()[0])` are valid only when the accessor returns the actual object stored in `cf.data`. This is always the case for inewave's accessor methods. Passing objects fetched from a different file instance to `remove()` will raise `ValueError` under cfinterface 1.9.0.

- **mypy passes at current non-strict level**: The project runs `mypy inewave/` without `--strict`. As of this epic, mypy reports 0 errors across 542 source files. Future epics that introduce strict mode (tickets 023-024) should tackle `newave` and `nwlistop` modules separately, since strict mode across the entire codebase would require too many changes at once.

## Surprises & Deviations

- **cfinterface 1.9.0 breaking behavioral change in RegisterData.\_index_of()**: The ticket stated that cfinterface 1.9.0 is "fully backward compatible" and that test failures were "unlikely." This was incorrect. cfinterface 1.9.0 changed `_index_of()` in `RegisterData`, `SectionData`, and `BlockData` from equality-based (`==`) to identity-based (`is`) lookup. This is a silent behavioral breaking change: it does not raise an error at import time, only at runtime when `remove()` or `add_before()` / `add_after()` is called with an object from a different container instance. Affected tests: `test_neq_eolica()` in `tests/libs/test_eolica.py` (line 252) and `test_neq_restricoes()` in `tests/libs/test_restricoes.py` (line 314). The same pattern (`cf2.data.remove(cf2.accessor()[0])`) exists in other test files -- those were already using the same instance, so they passed without change.

- **cfinterface 1.9.0 NaT bug in \_is_null()**: `math.isnan()` raises `TypeError` when called on `pandas.NaT` because NaT is not a float. cfinterface 1.8.0 did not have `_is_null()` at all (or had a different implementation), so this was never triggered. The fix wraps the `math.isnan()` call in a `try/except (TypeError, ValueError)` and adds a separate code path that detects datetime-like null sentinels by attempting `value.strftime("%Y")`. This fix lives in `/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py` and must be upstreamed to the cfinterface PyPI release.

- **Test count was 1066, not 430+**: The ticket and epic overview stated "430+ tests." The actual test run had 1066 tests. This gap suggests the test suite grew significantly since the plan was written, or the estimate was always an undercount. Future planning should use `pytest --collect-only -q | tail -1` to get the exact count.

- **cfinterface 1.9.0 was not on PyPI at implementation time**: The ticket's error-handling section anticipated this and specified the `[tool.uv.sources]` fallback. The fallback was indeed needed. The `[tool.uv.sources]` section remains in `pyproject.toml` and must be removed once cfinterface 1.9.0 is published to PyPI.

## Recommendations for Future Epics

- **When working on epic-02 (nwlistop TabularSection Adoption)**: The identity-based `remove()` behavior in cfinterface 1.9.0 affects any test that calls `cf.data.remove()` with an object retrieved from a different file instance. Search for this pattern with `grep -n "\.data\.remove(" tests/` before finalizing epic-02 tests. The `nwlistop` module uses `BlockData` (same family as `RegisterData`), so the same identity constraint applies.

- **When working on epic-02**: The `[tool.uv.sources]` override in `pyproject.toml` means the environment uses a local cfinterface build. Any new cfinterface API used in epic-02 (TabularSection, TabularParser) must be present in the local copy at `/home/rogerio/git/cfinterface/`. Verify this before starting ticket-004.

- **When planning the cfinterface 1.9.0 upstream release**: The `_is_null()` NaT fix in `/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py` must be included in the release. Without it, any inewave code that reads files containing `pandas.NaT` date values will raise `TypeError` in the cfinterface layer.

- **When working on epic-03 (Schema Versioning)**: cfinterface 1.9.0 introduces `VERSIONS`, `read(version=...)`, and `validate()`. These are new APIs with no 1.8.0 equivalent -- there are no migration regressions to worry about (unlike StorageType which had a deprecation path). Confirm the local cfinterface copy has these APIs before writing ticket-014 (survey).

- **When enabling mypy strict (tickets 023-024)**: At the current non-strict level, `mypy inewave/` passes with 0 errors on 542 source files. Do NOT attempt to enable strict mode across the entire package at once. The `inewave/newave/` module and the `inewave/nwlistop/` module should be tackled in separate tickets as specified in the plan. Each module contains hundreds of `# type: ignore` comments that will need to be resolved individually.
