# Accumulated Learnings: inewave Quality and Performance Upgrade

## Summary (through epic-01-foundation-and-storagetype-migration)

### Key Patterns

- **StorageType enum declaration**: Binary storage files declare `STORAGE = StorageType.BINARY` with `from cfinterface.storage import StorageType` placed in the cfinterface import group, before inewave imports. See any of the 16 files in `inewave/newave/` (e.g., `inewave/newave/hidr.py`, `inewave/newave/vazoes.py`).
- **uv local source override**: `[tool.uv.sources]` in `pyproject.toml` overrides PyPI resolution with a local path while keeping `dependencies` version-bounded; used while cfinterface 1.9.0 awaits PyPI release.
- **nwlistop/nwlistcf have no explicit STORAGE**: These modules inherit `StorageType.TEXT` from `BlockFile` and must not be given a redundant `STORAGE` attribute.

### Key Decisions

- **`>=` version bound, not `==` pin**: `pyproject.toml` uses `"cfinterface>=1.9.0"` because inewave is a library; forward compatibility matters more than strict reproducibility.
- **Fix cfinterface bugs upstream, not in inewave**: The `_is_null()` NaT bug was fixed in the local cfinterface copy (`/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py`), not papered over in inewave. This must be upstreamed before the cfinterface PyPI release.
- **mypy at non-strict level**: `mypy inewave/` runs without `--strict` and passes 0 errors on 542 source files. Strict mode for `newave` and `nwlistop` is deferred to tickets 023-024 and must be tackled per-module.

### Key Files

- `pyproject.toml`: Dependency floor is `"cfinterface>=1.9.0"` with `[tool.uv.sources]` local override; remove the override once cfinterface 1.9.0 ships to PyPI.
- `inewave/__init__.py`: Package version is `"1.13.0"`; Hatchling reads this as the canonical version.
- `inewave/newave/hidr.py`, `inewave/newave/vazoes.py`: Reference examples of the `StorageType.BINARY` import and declaration pattern (both `RegisterFile` subclasses); `SectionFile` subclass examples are in `inewave/newave/cortes.py`.
- `/home/rogerio/git/cfinterface/cfinterface/data/registerdata.py`: Contains the identity-based `_index_of()` (line 41-45) and `remove()` (line 110-122) that changed from equality to identity in cfinterface 1.9.0.
- `/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py`: Contains the NaT-safe `_is_null()` fix; must be upstreamed.

### Conventions

- **Import ordering**: `cfinterface` imports first (all adjacent), then `inewave` local imports, then `typing` imports last. `StorageType` import belongs in the cfinterface group.
- **No DeprecationWarning suppression**: Warnings must be eliminated at the source, not filtered via `filterwarnings` in `conftest.py`.
- **Test accessor objects are same-container**: `cf.data.remove(cf.accessor()[0])` is valid because inewave accessors return the stored instance. Passing an object from a different file instance to `remove()` raises `ValueError` under cfinterface 1.9.0.
- **Test count baseline**: Run `pytest --collect-only -q | tail -1` to get the actual count (1066 as of this epic, not the 430+ stated in the plan).

### Warnings

- **cfinterface 1.9.0 identity-based removal is a silent breaking change**: `RegisterData._index_of()` uses `is` (identity), not `==` (equality). Any code that calls `data.remove()`, `data.add_before()`, or `data.add_after()` with an object fetched from a different container instance will raise `ValueError`. The same applies to `SectionData` and `BlockData`. Search `tests/` for `\.data\.remove(` before finalizing any epic-02 tests.
- **cfinterface 1.9.0 has a NaT bug not yet on PyPI**: `math.isnan(pandas.NaT)` raises `TypeError`. The fix is in the local cfinterface copy only. Any inewave file that reads columns containing NaT values will fail if run against the (not-yet-released) PyPI build.
- **`[tool.uv.sources]` override must be removed before PyPI release**: The local path override in `pyproject.toml` will break installs for anyone without `/home/rogerio/git/cfinterface`. Remove it when cfinterface 1.9.0 is published.
- **cfinterface 1.9.0 "backward compatible" claim is partially wrong**: The StorageType change is backward compatible (string equality hash still works, just emits DeprecationWarning). The `_index_of()` equality-to-identity change is NOT backward compatible. Treat all cfinterface minor version bumps as potentially breaking for code using `remove()` / `add_before()` / `add_after()`.
