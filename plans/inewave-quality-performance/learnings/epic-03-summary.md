# Accumulated Learnings: inewave Quality and Performance Upgrade

## Summary (through epic-03-schema-versioning)

### Key Patterns

- **StorageType enum declaration**: Binary storage files declare `STORAGE = StorageType.BINARY` with `from cfinterface.storage import StorageType` placed in the cfinterface import group, before inewave imports. See any of the 16 files in `inewave/newave/` (e.g., `inewave/newave/hidr.py`, `inewave/newave/vazoes.py`).
- **uv local source override**: `[tool.uv.sources]` in `pyproject.toml` overrides PyPI resolution with a local path while keeping `dependencies` version-bounded; used while cfinterface 1.9.0 awaits PyPI release.
- **nwlistop/nwlistcf have no explicit STORAGE**: These modules inherit `StorageType.TEXT` from `BlockFile` and must not be given a redundant `STORAGE` attribute.
- **Block + TabularParser composition**: New nwlistop block base classes extend `Block` and compose `TabularParser` internally. Do NOT extend `TabularSection` (which is a `Section`) for `BlockFile`-based modules. See `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py` and `tabela_serie_patamar_anual.py`.
- **COLUMNS-only subclass definition**: Migrated nwlistop model files define only `COLUMNS = [ColumnDef(...), ...]`. Convention: first entry is `"serie"`, second (patamar variant) is `"patamar"`, then 12 month entries using `MESES_DF[i]`. See `inewave/nwlistop/modelos/earmf.py` and `cmarg.py`.
- **isinstance() dual-type guard in archive bases**: Archive base classes use `isinstance(b, (ValoresSerie, TabelaSerieAnual))` in `__monta_tabela()` rather than `of_type()`. This is forward-compatible and does not depend on cfinterface type registry internals. See `inewave/nwlistop/modelos/arquivos/arquivoree.py`.
- **Series carry-forward as static mutation**: `TabelaSeriePatamarAnual._apply_series_carry_forward()` mutates the parsed dict in-place before DataFrame construction. Default fill is `1`, not `None`. See `tabela_serie_patamar_anual.py` lines 112-124.
- **DeprecationWarning in `__init__` for replaced classes**: Old classes (`ValoresSerie`, `ValoresSeriePatamar`) emit `DeprecationWarning` with `stacklevel=2` and are retained (not deleted) because inewave is a library. See `inewave/nwlistop/modelos/blocos/valoresserie.py`.
- **VERSIONS declaration pattern**: Handler files declare `BLOCKS = [HeaderBlock, LatestBlock]` (latest/default) and `VERSIONS = { "older_key": [HeaderBlock, OlderBlock], "newer_key": [HeaderBlock, LatestBlock] }`. Lexicographic comparison (`<=`) determines which VERSIONS dict entry to use. See `inewave/nwlistop/cmarg.py` and `inewave/nwlistop/pivarm.py` for reference implementations.
- **Lexicographic version key convention**: Version keys are bare NEWAVE version strings (`"27"`, `"28"`, `"28.12"`, `"28.16"`, `"29.2"`, `"29.4.1"`) compared lexicographically, not semantically. `"28.12"` < `"28.16"` < `"28.2"` because `"12"` < `"16"` < `"2"` at the substring level. See `version-catalog.md` for a complete lexicographic ordering table.
- **read(version=...) replaces set_version()**: Modern API is `handler.read(path, version="27")` instead of deprecated `handler.set_version("27"); handler.read(path)`. The new API does NOT mutate class-level state and makes version selection explicit at the call site. See test migrations in `tests/nwlistop/test_cmarg.py`, `test_cmargmed.py`, `test_pivarm.py`, `test_pivarmincr.py`.
- **validate() is inherited and sufficient**: cfinterface's inherited `validate()` method on BlockFile/SectionFile checks whether parsed data matches expected component types for a version. No custom implementation needed in inewave. Returns `VersionMatchResult(matched: bool, missing_types: List, unexpected_types: List, default_ratio: float)`. See ticket-017 findings.
- **Zero new VERSIONS needed**: The complete version audit in version-catalog.md found that all known format differences are already handled by the 5 existing versioned files (cmarg, cmargmed, pivarm, pivarmincr, avl_cortesfpha_nwv). No additional nwlistop BlockFile, newave SectionFile, newave BlockFile, or newave RegisterFile requires VERSIONS.

### Key Decisions

- **`>=` version bound, not `==` pin**: `pyproject.toml` uses `"cfinterface>=1.9.0"` because inewave is a library; forward compatibility matters more than strict reproducibility.
- **Fix cfinterface bugs upstream, not in inewave**: The `_is_null()` NaT bug was fixed in the local cfinterface copy (`/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py`), not papered over in inewave. Must be upstreamed before cfinterface PyPI release.
- **mypy at non-strict level**: `mypy inewave/` runs without `--strict` and passes 0 errors on 544 source files. Strict mode for `newave` and `nwlistop` is deferred to tickets 023-024.
- **Exclude `gtert.py` from TabularSection migration**: `ValoresClasseTermicaSeriePatamar` has 3-level grouping (classe + serie + patamar) and MEDIA/MAX sentinel handling; it cannot be expressed in the 2-level base classes. It remains on the old block type indefinitely. See `inewave/nwlistop/modelos/gtert.py`.
- **Extend Block, not TabularSection**: Using `TabularSection` (a `Section`) inside a `BlockFile` violates cfinterface lifecycle. The accepted approach is `TabularParser` composition inside `Block`.
- **BLOCKS list unchanged in archive bases**: Archive base classes retain `BLOCKS = [HeaderBlock, ValoresSerie]`. The actual block type is resolved at the concrete model file level. This avoids touching cfinterface dispatch.
- **No deletion of old block classes**: `ValoresSerie` and `ValoresSeriePatamar` kept with deprecation warnings; deletion deferred to a future major version.
- **Version-variant classes named with suffix**: Use suffix `_v<major>_<minor>` (e.g., `PivarmAnos_v29_2`) or version number (e.g., `CmargsAnos27`, `CmargsAnos28`). Naming convention varies per file but must be consistent within each file. See model files for reference.
- **No detect_version() helper needed**: Inherited `validate()` is sufficient for downstream use. Version information is typically known from NEWAVE context rather than needing automatic detection. Users call `handler.validate(version="known_version")` directly. See ticket-017 findings.
- **Graceful degradation for unconfirmed variants**: Files with suspected but unconfirmed version differences (dger, pmo, patamar, sistema) degrade gracefully via keyword-based section/block matching. Missing sections/blocks return None rather than failing. Confirmation requires testing against actual output from different NEWAVE versions.

### Key Files

- `pyproject.toml`: Dependency floor is `"cfinterface>=1.9.0"` with `[tool.uv.sources]` local override; remove the override once cfinterface 1.9.0 ships to PyPI.
- `inewave/__init__.py`: Package version is `"1.13.0"`; Hatchling reads this as the canonical version.
- `inewave/newave/hidr.py`, `inewave/newave/vazoes.py`: Reference examples of `StorageType.BINARY` import and declaration pattern.
- `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`: Base class for ValoresSerie family (77+ subclasses). 113 LOC. Defines `COLUMNS`, `_build_dataframe()`, `_tidy_to_wide()`.
- `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py`: Base class for ValoresSeriePatamar family (87+ subclasses). 156 LOC. Adds series carry-forward and `_blank_serie_field()`.
- `inewave/nwlistop/modelos/earmf.py`: Reference example of a migrated `TabelaSerieAnual` subclass.
- `inewave/nwlistop/modelos/cmarg.py`: Reference example of a migrated `TabelaSeriePatamarAnual` subclass with version-variant classes (`CmargsAnos27`, `CmargsAnos`).
- `inewave/nwlistop/modelos/pivarm.py`: Demonstrates `FloatField(format="E")` for format-variant (VERSIONS) blocks. Version-variant classes: `PivarmAnos` (decimal), `PivarmAnos_v29_2` (scientific).
- `inewave/nwlistop/modelos/arquivos/arquivoree.py`: Reference archive base with isinstance() dual-type guard.
- `inewave/nwlistop/cmarg.py`: Reference handler with VERSIONS dictionary. Pattern: `BLOCKS = [Submercado, CmargsAnos]`, `VERSIONS = { "27": [...], "29.4.1": [...] }`.
- `inewave/nwlistop/pivarm.py`: Reference handler with format-variant VERSIONS using `format="E"`.
- `inewave/newave/avl_cortesfpha_nwv.py`: Reference newave BlockFile with VERSIONS. Demonstrates version-specific section/block class combinations.
- `plans/inewave-quality-performance/version-catalog.md`: Comprehensive 417-line audit of all versioned and unversioned files. Documents 5 already-versioned files, explains lexicographic key convention with ordering table, confirms 0 new nwlistop files need VERSIONS, confirms 0 new newave files need VERSIONS, lists 4 open questions for unconfirmed variants, provides rationale for each category decision.
- `tests/nwlistop/test_tabela_serie_anual.py`: Unit tests for `TabelaSerieAnual` (318 LOC); defines `EarmsAnosTSA` test subclass convention.
- `tests/nwlistop/test_tabela_serie_patamar_anual.py`: Unit tests for `TabelaSeriePatamarAnual` (433 LOC); defines `CmargsAnosTSPA` test subclass convention.
- `tests/nwlistop/test_cmarg.py`: Migrated test file using `read(path, version="27")` instead of `set_version()`. Includes validate() tests.
- `tests/nwlistop/test_cmargmed.py`: Migrated test file with version tests and validate() tests.
- `tests/nwlistop/test_pivarm.py`: Migrated test file demonstrating format-variant testing (decimal vs scientific notation).
- `tests/nwlistop/test_pivarmincr.py`: Migrated test file.
- `tests/newave/test_avl_cortesfpha_nwv.py`: Migrated newave version tests.
- `tests/mocks/arquivos/cmarg.py`: Mock data with version-specific constants: `MockCmarg27`, `MockCmarg`.
- `tests/mocks/arquivos/pivarm.py`: Mock data: `MockPivarm`, `MockPivarm_v29_2`.
- `/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py`: Contains the NaT-safe `_is_null()` fix; must be upstreamed.
- `/home/rogerio/git/cfinterface/cfinterface/versioning.py`: `resolve_version()` (lexicographic comparison), `validate_version()` (type matching), `VersionMatchResult` (result type).

### Conventions

- **Import ordering**: `cfinterface` imports first (all adjacent), then `inewave` local imports, then `typing` imports last. `StorageType` import belongs in the cfinterface group.
- **No DeprecationWarning suppression**: Warnings must be eliminated at the source, not filtered via `filterwarnings` in `conftest.py`.
- **Test accessor objects are same-container**: `cf.data.remove(cf.accessor()[0])` is valid because inewave accessors return the stored instance. Passing an object from a different file instance to `remove()` raises `ValueError` under cfinterface 1.9.0.
- **COLUMNS naming is load-bearing**: `"serie"`, `"patamar"`, and `MESES_DF[i]` names in `ColumnDef` are used by `_build_dataframe()` and `_tidy_to_wide()` via dict key lookup. Deviating from these names silently breaks DataFrame construction.
- **Test subclass naming suffix**: Test-only block subclasses in test files use `TSA` suffix (TabelaSerieAnual) or `TSPA` suffix (TabelaSeriePatamarAnual), e.g., `EarmsAnosTSA`, `CmargsAnosTSPA`.
- **`__slots__ = []` on every subclass**: All block subclasses declare `__slots__ = []` to preserve memory layout. This is mandatory across all nwlistop model files.
- **Plan for a cleanup pass after batch migrations**: Automated batch migrations introduce AI bloat (redundant docstrings, over-engineered helpers). Explicitly budget a code-simplifier pass after each batch ticket group.
- **VERSIONS key naming**: Use NEWAVE version numbers as bare strings (`"27"`, `"28"`, `"28.12"`, `"28.16"`, `"29.2"`, `"29.4.1"`). No "v" prefix. Order keys from oldest to newest for readability.
- **read(version=...) convention**: Pass version as keyword argument to read() method rather than using deprecated `set_version()`. Pattern: `handler.read(path, version="27")`.
- **validate() convention**: Call `handler.validate(version=known_version)` to verify parsed data matches expected types. The inherited method returns a `VersionMatchResult` with matched (bool), missing_types, unexpected_types, and default_ratio.
- **Version-variant model class naming**: Use suffix `_v<major>_<minor>` (e.g., `PivarmAnos_v29_2`) or version number (e.g., `CmargsAnos27`, `CmargsAnos28`). Be consistent within each file but may vary across files.

### Warnings

- **cfinterface 1.9.0 identity-based removal is a silent breaking change**: `RegisterData._index_of()` uses `is` (identity), not `==` (equality). Any code that calls `data.remove()`, `data.add_before()`, or `data.add_after()` with an object fetched from a different container instance will raise `ValueError`. Search `tests/` for `\.data\.remove(` before any epic involving those methods.
- **cfinterface 1.9.0 has a NaT bug not yet on PyPI**: `math.isnan(pandas.NaT)` raises `TypeError`. The fix is in the local cfinterface copy only.
- **`[tool.uv.sources]` override must be removed before PyPI release**: The local path override in `pyproject.toml` will break installs for anyone without `/home/rogerio/git/cfinterface`.
- **cfinterface 1.9.0 "backward compatible" claim is partially wrong**: The `_index_of()` equality-to-identity change is NOT backward compatible. Treat all cfinterface minor version bumps as potentially breaking for code using `remove()` / `add_before()` / `add_after()`.
- **mypy strict will require `ClassVar` on `COLUMNS`**: The current `COLUMNS: List[ColumnDef] = []` annotation on both new base classes will need `ClassVar[List[ColumnDef]]` to pass `--strict`. Plan for this in tickets 023-024.
- **Test count baseline is 1126, not 430+**: The plan documents "430+ tests" from an outdated count. The actual baseline as of epic-02 completion is 1126 tests (`pytest --collect-only -q`). After epic-03, with 8 new validate() tests added, the count is 1134.
- **Snapshot LOC before batch migrations**: The plan assumed ">30% LOC reduction" but no pre-migration LOC baseline was recorded. Always capture `wc -l` totals before starting a batch migration epic.
- **Lexicographic version key comparison is counterintuitive**: `"28.12"` sorts before `"28.2"` lexicographically. Do not "fix" this to semantic versioning. The existing codebase intentionally uses this convention and has selected version keys that avoid ambiguity (e.g., does not use both `"28.1"` and `"28.10"` which would sort in unexpected order).
- **Unconfirmed version candidates need real-world testing**: dger, pmo, patamar, and sistema may have graceful degradation for older NEWAVE versions, but confirmation requires parsing actual files from pre-v28 and current versions. Do not assume graceful degradation without evidence.
