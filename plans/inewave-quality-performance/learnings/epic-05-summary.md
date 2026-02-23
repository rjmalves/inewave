# Accumulated Learnings: inewave Quality and Performance Upgrade

## Summary (through epic-05-quality-and-type-safety)

### Key Patterns

- **StorageType enum declaration**: Binary storage files declare `STORAGE = StorageType.BINARY` with `from cfinterface.storage import StorageType` in the cfinterface import group. See `inewave/newave/hidr.py`, `inewave/newave/vazoes.py`.
- **nwlistop/nwlistcf have no explicit STORAGE**: These inherit `StorageType.TEXT` from `BlockFile`; adding a redundant attribute breaks dispatch.
- **Block + TabularParser composition**: New nwlistop block base classes extend `Block` and compose `TabularParser` internally. Do NOT extend `TabularSection` for `BlockFile`-based modules. See `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`.
- **COLUMNS-only subclass definition**: Migrated nwlistop model files define only `COLUMNS = [ColumnDef(...), ...]`. Names `"serie"`, `"patamar"`, and `MESES_DF[i]` are load-bearing for `_build_dataframe()`. See `inewave/nwlistop/modelos/earmf.py` and `cmarg.py`.
- **isinstance() dual-type guard in archive bases**: `_monta_tabela()` uses `isinstance(b, self._DATA_BLOCK_TYPES)` where `_DATA_BLOCK_TYPES` is a tuple class variable. See `inewave/nwlistop/modelos/arquivos/_base_serie.py` line 30.
- **Collect-then-concat in `_monta_tabela()`**: Both base classes use a list comprehension to collect DataFrames then call `pd.concat(dfs, ignore_index=True)` once. See `inewave/nwlistop/modelos/arquivos/_base_serie.py`.
- **PEP 562 lazy import pattern**: `inewave/nwlistop/__init__.py` and `inewave/newave/__init__.py` replace eager imports with `_LAZY_IMPORTS: dict[str, str]`, `__all__ = sorted(...)`, `def __getattr__(name: str) -> Any:`, and `def __dir__() -> list[str]: return __all__`.
- **`__dir__` required alongside `__getattr__`**: Without `__dir__`, `dir(inewave.nwlistop)` returns only already-cached names.
- **`globals()[name] = value` caching eliminates repeat `__getattr__` calls**: After first access, the resolved class is stored directly in the module namespace.
- **VERSIONS declaration pattern**: Handler files use `BLOCKS = [HeaderBlock, LatestBlock]` and `VERSIONS = { "version_key": [...], ... }`. Lexicographic `<=` determines block selection. See `inewave/nwlistop/cmarg.py`.
- **Series carry-forward as static mutation**: `TabelaSeriePatamarAnual._apply_series_carry_forward()` mutates the parsed dict in-place; default fill is `1`. See `tabela_serie_patamar_anual.py`.
- **DeprecationWarning in `__init__` for replaced classes**: `ValoresSerie` / `ValoresSeriePatamar` emit warnings at `stacklevel=2` and are not deleted. See `inewave/nwlistop/modelos/blocos/valoresserie.py`.
- **`IO[Any]` over `IO[str]` for all read/write overrides**: cfinterface's `Line.write()` returns `Union[str, bytes]`, making `IO[str]` incorrect at the library boundary. All 418 `[override]` annotations use `IO[Any]`. See `inewave/newave/modelos/dger.py`.
- **`# type: ignore[override]` on every read/write subclass method**: cfinterface base returns `bool`, inewave subclasses return `None`. The incompatibility is inherent to the library boundary. 418 instances, all with explanation comments.
- **`Optional[Any]` for cfinterface `__init__` parameters**: All Section/Block `__init__` overrides use `previous: Optional[Any] = None, next: Optional[Any] = None, data: Optional[Any] = None`. See `inewave/newave/modelos/dger.py`.
- **`-> Any` on `__getattr__` in lazy import `__init__.py`**: Both `inewave/newave/__init__.py` line 88 and `inewave/nwlistop/__init__.py` line 183 require this annotation under strict mode.
- **`_DATA_BLOCK_TYPES` tuple for archive configuration**: `_ArquivoSerieBase` and `_ArquivoSeriePatamarBase` expose `_DATA_BLOCK_TYPES: tuple[type, ...]` as a class variable. Subclasses override it to change isinstance dispatch. See `inewave/nwlistop/modelos/arquivos/_base_serie.py` and `arquivoclassetermicasubmercadopatamar.py`.
- **`cast(Iterable[Block], self.data)` for type narrowing in base classes**: Avoids suppressing errors in the loop body. See `inewave/nwlistop/modelos/arquivos/_base_serie.py` line 29.
- **`# type: ignore[import-untyped]` for all pandas/numpy imports**: 138 instances. Pandas 2.2.3 and numpy 2.2.1 do NOT provide stubs recognized by mypy. Bare ignores were replaced. Explanation: `# no pandas-stubs package`.
- **Phase-level instrumentation via monkey-patching**: `benchmarks/profile_read.py` measures per-phase timing by wrapping `TabularParser.parse_lines`, `TabelaSerieAnual._build_dataframe`, and `formata_df_meses_para_datas_nwlistop`.

### Key Decisions

- **`>=` version bound, not `==` pin**: `pyproject.toml` uses `"cfinterface>=1.9.0"` because inewave is a library.
- **Fix cfinterface bugs upstream, not in inewave**: The `_is_null()` NaT bug fix lives in the local cfinterface copy; must be upstreamed before PyPI release.
- **`warn_return_any = false` globally and per-module**: cfinterface's `Section.data` and `Block.data` are `Any`-typed. Enabling `warn_return_any = true` would produce 528+ meaningless errors from every property that reads `self.data[N]`. All strict overrides in `pyproject.toml` include `warn_return_any = false`.
- **`IO[Any]` not `IO[str]`**: Using `IO[str]` caused 193 errors due to `Line.write()` returning `Union[str, bytes]`. Rejected both `IO[str]` and `IO[bytes]`; adopted `IO[Any]` uniformly.
- **Two distinct base classes for series vs patamar archives**: `_ArquivoSerieBase` and `_ArquivoSeriePatamarBase` not merged. Data-shape difference is fundamental to the public API contract. See `inewave/nwlistop/modelos/arquivos/_base_serie.py` and `_base_serie_patamar.py`.
- **`_get_header_value()` helper omitted from base classes**: The ticket-025 design proposed this helper; actual implementation keeps header access in each subclass property using `self.data.get_blocks_of_type(HeaderType)`. Simpler and does not require the base to import all header block types.
- **No deletion of old block classes**: `ValoresSerie` / `ValoresSeriePatamar` kept with deprecation warnings; deletion deferred to a future major version.
- **Exclude `gtert.py` from TabularSection migration**: 3-level grouping (classe + serie + patamar) cannot be expressed in the 2-level base classes.
- **`nwlistcf/__init__.py` excluded from lazy import conversion**: Only 5 imports; overhead is negligible.
- **No pytest-benchmark or asv**: Benchmark suite uses only stdlib, run on demand.
- **Profiling before optimizing**: Ticket-019 was a hard prerequisite for 020-021. Profiling revealed `TabularParser.parse_lines` at 28-32% of nwlistop read time.
- **Zero new VERSIONS needed**: The version audit confirmed no additional files require VERSIONS beyond the 5 already versioned.
- **Strict mypy scope covers all production code**: All of `inewave/newave`, `inewave/nwlistop`, `inewave/nwlistcf`, `inewave/_utils`, `inewave/libs`. `benchmarks/` is excluded.

### Key Files

- `pyproject.toml`: Dependency floor `"cfinterface>=1.9.0"`; `[tool.mypy]` section with 8 `[[tool.mypy.overrides]]` blocks, all `strict = true, warn_return_any = false`.
- `inewave/__init__.py`: Package version `"1.13.0"`.
- `inewave/newave/__init__.py`: Lazy import module — `_LAZY_IMPORTS` dict (76 entries), `__getattr__(name: str) -> Any:`, `__dir__`.
- `inewave/nwlistop/__init__.py`: Lazy import module — `_LAZY_IMPORTS` dict (171 entries), same pattern.
- `inewave/nwlistop/modelos/arquivos/_base_serie.py`: `_ArquivoSerieBase` (51 lines). Canonical thin-base pattern for series-only archives.
- `inewave/nwlistop/modelos/arquivos/_base_serie_patamar.py`: `_ArquivoSeriePatamarBase` (59 lines). Canonical thin-base pattern for patamar archives.
- `inewave/nwlistop/modelos/arquivos/arquivoree.py`: Reference thin-subclass after refactor (28 lines). Shows `_HEADER_BLOCK`-less design with inline `get_blocks_of_type` property.
- `inewave/nwlistop/modelos/arquivos/arquivoclassetermicasubmercadopatamar.py`: Reference for overriding `_DATA_BLOCK_TYPES` in a subclass.
- `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`: Base class for 77+ migrated model subclasses. Reference for `COLUMNS: ClassVar[List[ColumnDef]]` and `_build_dataframe()`.
- `inewave/newave/modelos/dger.py`: Canonical annotation pattern for Section subclasses — `Optional[Any]` init params, `IO[Any]` read/write with `[override]`, `-> None` setters.
- `benchmarks/profile_read.py`: Phase-level profiling with monkey-patch instrumentation.
- `benchmarks/benchmark_results.md`: Current baseline for regression detection.
- `plans/inewave-quality-performance/version-catalog.md`: 417-line audit of versioned/unversioned files.

### Conventions

- **Import ordering**: `cfinterface` imports first, then `inewave` local imports, then `typing` last.
- **No DeprecationWarning suppression**: Warnings must be eliminated at the source.
- **`__slots__: list[str] = []` on every archive subclass**: Python 3.9+ lowercase `list` form, empty list.
- **VERSIONS key naming**: Bare NEWAVE version strings (`"27"`, `"28"`). Lexicographic comparison.
- **read(version=...) convention**: `handler.read(path, version="27")` instead of deprecated `set_version()`.
- **All property setters annotated `-> None`**: Mandatory under strict mode.
- **All nested conversion functions annotated**: `-> pd.DataFrame` or appropriate type on private inner functions.
- **`# type: ignore` always has specific code and inline explanation**: Zero bare ignores remain in `inewave/`. Template: `# type: ignore[code]  # brief reason`.
- **`_LAZY_IMPORTS` dict key ordering**: Deprecated entries at top, then active handlers in original import order. `__all__ = sorted(...)` for deterministic `dir()`.
- **Test baseline is 1134 tests**: As of epic-05 completion.
- **Benchmark handler/mock loading always via `importlib.import_module`**: Never import inewave at benchmark module top-level.
- **Plan for a cleanup pass after batch migrations**: Batch migrations introduce AI bloat. Explicitly budget a code-simplifier pass after each batch ticket group.

### Warnings

- **cfinterface 1.9.0 identity-based removal is a silent breaking change**: `_index_of()` uses `is` not `==`. Search `tests/` for `\.data\.remove(` before any epic using those methods.
- **cfinterface 1.9.0 NaT bug not yet on PyPI**: `math.isnan(pandas.NaT)` raises `TypeError`. Fix in local cfinterface copy only. Remove `[tool.uv.sources]` override before PyPI release.
- **`IO[Any]` convention depends on cfinterface `Line.write()` return type**: If cfinterface is updated to return `str` only, the 418 `[override]` ignores may become `unused-ignore`. Run `mypy inewave/ --strict` after any cfinterface upgrade.
- **pandas/numpy do NOT provide stubs recognized by mypy** at 2.2.x versions: `# type: ignore[import-untyped]` is still required on every `import pandas as pd` and `import numpy as np`. Do not remove these.
- **`benchmarks/` is outside mypy strict scope**: Benchmark files carry their own unvalidated `# type: ignore` comments. Add a `[[tool.mypy.overrides]]` for `benchmarks` if type-checking is desired.
- **Lexicographic version key comparison is counterintuitive**: `"28.12"` sorts before `"28.2"`. Do not "fix" to semantic versioning.
- **`__monta_tabela` aggregation time is zero with single-year mock data**: The O(n^2) fix from ticket-020 is invisible in benchmark results. The improvement only manifests on real NEWAVE output files with 20+ blocks.
- **Snapshot LOC before batch migrations**: Always capture `wc -l` totals before starting a batch migration epic.
- **cfinterface minor version bumps may be breaking**: Treat all minor bumps as potentially breaking for `remove()` / `add_before()` / `add_after()` code.
