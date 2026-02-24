# Accumulated Learnings: inewave Quality and Performance Upgrade

## Summary (through epic-07-documentation — FINAL)

### Key Patterns

- **StorageType enum declaration**: Binary storage files declare `STORAGE = StorageType.BINARY` with `from cfinterface.storage import StorageType` in the cfinterface import group. See `inewave/newave/hidr.py`, `inewave/newave/vazoes.py`.
- **nwlistop/nwlistcf have no explicit STORAGE**: These inherit `StorageType.TEXT` from `BlockFile`; adding a redundant attribute breaks dispatch.
- **Block + TabularParser composition**: New nwlistop block base classes extend `Block` and compose `TabularParser` internally. Do NOT extend `TabularSection` for `BlockFile`-based modules. See `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`.
- **COLUMNS-only subclass definition**: Migrated nwlistop model files define only `COLUMNS = [ColumnDef(...), ...]`. Names `"serie"`, `"patamar"`, and `MESES_DF[i]` are load-bearing for `_build_dataframe()`. See `inewave/nwlistop/modelos/earmf.py` and `cmarg.py`.
- **Collect-then-concat in `_monta_tabela()`**: Both base classes use a list comprehension to collect DataFrames then call `pd.concat(dfs, ignore_index=True)` once. See `inewave/nwlistop/modelos/arquivos/_base_serie.py`.
- **PEP 562 lazy import pattern**: `inewave/nwlistop/__init__.py` and `inewave/newave/__init__.py` replace eager imports with `_LAZY_IMPORTS: dict[str, str]`, `__all__ = sorted(...)`, `def __getattr__(name: str) -> Any:`, and `def __dir__() -> list[str]: return __all__`.
- **`globals()[name] = value` caching eliminates repeat `__getattr__` calls**: After first access, the resolved class is stored directly in the module namespace.
- **VERSIONS declaration pattern**: Handler files use `BLOCKS = [HeaderBlock, LatestBlock]` and `VERSIONS = { "version_key": [...], ... }`. Lexicographic `<=` determines block selection. See `inewave/nwlistop/cmarg.py`.
- **DeprecationWarning in `__init__` for replaced classes**: `ValoresSerie` / `ValoresSeriePatamar` emit warnings at `stacklevel=2` and are not deleted. See `inewave/nwlistop/modelos/blocos/valoresserie.py`.
- **`IO[Any]` over `IO[str]` for all read/write overrides**: cfinterface's `Line.write()` returns `Union[str, bytes]`, making `IO[str]` incorrect at the library boundary. All 418 `[override]` annotations use `IO[Any]`.
- **`# type: ignore[override]` on every read/write subclass method**: cfinterface base returns `bool`, inewave subclasses return `None`. 418 instances, all with explanation comments.
- **Phase-level instrumentation via monkey-patching**: `benchmarks/profile_read.py` measures per-phase timing by wrapping `TabularParser.parse_lines`, `TabelaSerieAnual._build_dataframe`, and `formata_df_meses_para_datas_nwlistop`.
- **tempfile round-trip for parametrized binary readers**: When `read()` requires external dimensions, use `tempfile.NamedTemporaryFile(delete=False)` + `os.unlink(tmp)` in a try/finally block. See `tests/newave/test_engnat.py` lines 72-91.
- **NOTE comment as skip-documentation for impossible tests**: Files where round-trip tests are architecturally impossible end with `# NOTE: {reason}, round-trip test not applicable`. See `tests/newave/test_energiab.py`, `test_pmo.py`.
- **Import aliasing to resolve model-class name collisions in tests**: When two handlers share identically-named model classes, use `as`-aliases. See `tests/nwlistop/test_version_validate.py` lines 25-32.
- **Repo-root Markdown for migration guides**: User-facing migration documentation lives at `/MIGRATION.md` as a standalone Markdown file, not part of the sphinx build. See `/home/rogerio/git/inewave/MIGRATION.md`.
- **Audience-based language split in documentation**: User-facing docs (`MIGRATION.md`, `CHANGELOG.md`, `docs/`) in Portuguese; developer-facing infrastructure docs (`benchmarks/README.md`) in English, matching existing artifact language.
- **Curated key-numbers section in benchmark README**: `benchmarks/README.md` provides synthesised headline numbers with a Markdown table and explicit reliability caveats for each known measurement artefact. See `benchmarks/README.md` lines 108-209.

### Key Decisions

- **`>=` version bound, not `==` pin**: `pyproject.toml` uses `"cfinterface>=1.9.0"` because inewave is a library. `pytest-xdist` added with same pattern.
- **Fix cfinterface bugs upstream, not in inewave**: The `_is_null()` NaT bug fix lives in the local cfinterface copy; must be upstreamed before PyPI release.
- **`IO[Any]` not `IO[str]`**: Using `IO[str]` caused 193 errors due to `Line.write()` returning `Union[str, bytes]`. Adopted `IO[Any]` uniformly.
- **Two distinct base classes for series vs patamar archives**: `_ArquivoSerieBase` and `_ArquivoSeriePatamarBase` not merged. Data-shape difference is fundamental to the public API contract.
- **No deletion of old block classes**: `ValoresSerie` / `ValoresSeriePatamar` kept with deprecation warnings; deletion deferred to a future major version.
- **Exclude `gtert.py` from TabularSection migration**: 3-level grouping (classe + serie + patamar) cannot be expressed in the 2-level base classes.
- **`nwlistcf/__init__.py` excluded from lazy import conversion**: Only 5 imports; overhead is negligible.
- **Zero new VERSIONS needed beyond the 5 already versioned**: Version audit (ticket-014) confirmed no additional files require VERSIONS.
- **Strict mypy scope covers all production code**: All of `inewave/newave`, `inewave/nwlistop`, `inewave/nwlistcf`, `inewave/_utils`, `inewave/libs`. `benchmarks/` excluded.
- **`-n auto` NOT set as pytest default**: Parallel execution is opt-in. Default sequential run is safer for debugging.
- **Permanently-skipped tests are dead code**: `@pytest.mark.skip` implies fixability; NOTE comments are correct for architecturally impossible tests.
- **ticket-032 (sphinx autodoc) merged into ticket-031**: Codebase investigation showed RST pages auto-generate from already-accurate docstrings. Zero RST content changes needed.
- **MIGRATION.md not added to sphinx toctree**: Kept as standalone repo-root document for compatibility with GitHub/PyPI display conventions.
- **`set_version()` preserved without deprecation timeline**: Conservative API stability policy; `read(version=...)` is documented as preferred but `set_version()` is not deprecated.

### Key Files

- `pyproject.toml`: Dependency floor `"cfinterface>=1.9.0"`; `[tool.mypy]` with 8 overrides, all `strict = true, warn_return_any = false`; `[tool.pytest.ini_options]` with `testpaths`, `filterwarnings`; `pytest-xdist` in dev extras.
- `inewave/__init__.py`: Package version `"1.13.0"`.
- `inewave/newave/__init__.py`: Lazy import module — `_LAZY_IMPORTS` dict (76 entries), `__getattr__(name: str) -> Any:`, `__dir__`.
- `inewave/nwlistop/__init__.py`: Lazy import module — `_LAZY_IMPORTS` dict (171 entries), same pattern.
- `inewave/nwlistop/modelos/arquivos/_base_serie.py`: `_ArquivoSerieBase` (51 lines). Canonical thin-base pattern for series-only archives.
- `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`: Base class for 77+ migrated model subclasses.
- `inewave/newave/modelos/dger.py`: Canonical annotation pattern for Section subclasses.
- `benchmarks/profile_read.py`: Phase-level profiling with monkey-patch instrumentation.
- `benchmarks/benchmark_results.md`: Current baseline for regression detection. Do not edit by hand.
- `benchmarks/README.md`: Entry-point documentation for the benchmark suite; includes reliability caveats.
- `MIGRATION.md`: Six-section user-facing migration guide in Portuguese for v1.13.0.
- `CHANGELOG.md`: v1.13.0 entry prepended with 11 bullet points in Portuguese.
- `docs/source/geral/tutorial.rst`: Updated to document `read(version=...)` as preferred idiom (lines 125-153).
- `tests/newave/test_engnat.py`: Canonical tempfile round-trip pattern for parametrized binary SectionFile handlers.
- `tests/nwlistop/test_version_validate.py`: All 12 version/validate tests — 8 original + 4 new (Cmargmed, Pivarmincr).

### Conventions

- **Import ordering**: `cfinterface` imports first, then `inewave` local imports, then `typing` last.
- **`__slots__: list[str] = []` on every archive subclass**: Python 3.9+ lowercase `list` form, empty list.
- **VERSIONS key naming**: Bare NEWAVE version strings (`"27"`, `"28"`). Lexicographic comparison.
- **`read(version=...)` convention**: `handler.read(path, version="27")` instead of deprecated `set_version()`.
- **`# type: ignore` always has specific code and inline explanation**: Zero bare ignores remain in `inewave/`.
- **Round-trip test naming**: `test_leitura_escrita_{handler_name_lowercase}` — 34 total in `tests/newave/`.
- **NOTE comment format**: `# NOTE: {reason}, round-trip test not applicable` — at final line of file after blank line.
- **Test baseline is 1140 tests**: As of epic-06 completion.
- **Parallel test baseline**: 24.27s (`-n auto`), 59.53s (sequential) — 2.45x speedup on development machine.
- **MIGRATION.md section ordering**: Dependencies, non-breaking API additions, deprecations, internal changes, performance, testing — prioritises user actions first.
- **Version key table in MIGRATION.md**: All versioned classes listed in a single table (section 2.2); must be kept in sync with VERSIONS dicts in future PRs.
- **"Do not edit by hand" label on generated benchmark files**: `benchmark_results.md` and `profile_report.md` are overwritten by benchmark runners; the README labels them explicitly.

### Warnings

- **cfinterface 1.9.0 NaT bug not yet on PyPI**: `math.isnan(pandas.NaT)` raises `TypeError`. Fix in local cfinterface copy only. Remove `[tool.uv.sources]` override before PyPI release.
- **`IO[Any]` convention depends on cfinterface `Line.write()` return type**: If cfinterface is updated to return `str` only, the 418 `[override]` ignores may become `unused-ignore`.
- **pandas/numpy do NOT provide stubs recognized by mypy** at 2.2.x versions: `# type: ignore[import-untyped]` is still required on every `import pandas as pd` and `import numpy as np`.
- **Lexicographic version key comparison is counterintuitive**: `"28.12"` sorts before `"28.2"`. Do not "fix" to semantic versioning.
- **`__monta_tabela` aggregation time is zero with single-year mock data**: The O(n^2) fix from ticket-020 is invisible in benchmark results. The improvement only manifests on real NEWAVE output files with 20+ blocks.
- **cfinterface minor version bumps may be breaking**: Treat all minor bumps as potentially breaking for `remove()` / `add_before()` / `add_after()` code.
- **Audit write() before scoping round-trip tests**: 93% of planned newave round-trip targets had `Block.write()` raising `NotImplementedError`. Grep for `NotImplementedError` before scoping any round-trip testing epic.
- **`@pytest.mark.skip` implies a fixable test**: Use NOTE comments for architecturally impossible tests. Skip decorators mislead future developers.
- **nwlistop DeprecationWarning count depends on which handlers are exercised**: With lazy loading, only handlers reached by tests emit warnings. Warning counts in projections should be treated as upper bounds.
- **Sphinx autodoc pages may not need changes after large refactors**: If earlier epics update docstrings as they go, a dedicated documentation-cleanup ticket may find zero RST work remaining. Validate with a codebase investigation pass before budgeting docstring tickets.
- **Version key table in MIGRATION.md drifts from VERSIONS dicts if not updated in the same PR**: No automated check enforces sync between the two; discipline at PR review time is the only safeguard.
