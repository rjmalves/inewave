# Accumulated Learnings: inewave Quality and Performance Upgrade

## Summary (through epic-04-performance-optimization)

### Key Patterns

- **StorageType enum declaration**: Binary storage files declare `STORAGE = StorageType.BINARY` with `from cfinterface.storage import StorageType` in the cfinterface import group. See `inewave/newave/hidr.py`, `inewave/newave/vazoes.py`.
- **nwlistop/nwlistcf have no explicit STORAGE**: These inherit `StorageType.TEXT` from `BlockFile`; adding a redundant attribute breaks dispatch.
- **Block + TabularParser composition**: New nwlistop block base classes extend `Block` and compose `TabularParser` internally. Do NOT extend `TabularSection` for `BlockFile`-based modules. See `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`.
- **COLUMNS-only subclass definition**: Migrated nwlistop model files define only `COLUMNS = [ColumnDef(...), ...]`. Names `"serie"`, `"patamar"`, and `MESES_DF[i]` are load-bearing for `_build_dataframe()`. See `inewave/nwlistop/modelos/earmf.py` and `cmarg.py`.
- **isinstance() dual-type guard in archive bases**: `__monta_tabela()` uses `isinstance(b, (ValoresSerie, TabelaSerieAnual))` — not `of_type()` — for forward compatibility. See `inewave/nwlistop/modelos/arquivos/arquivoree.py`.
- **Collect-then-concat in `__monta_tabela()`**: All 13 archive base classes now use a list comprehension to collect DataFrames, then call `pd.concat(dfs, ignore_index=True)` once. The previous O(n^2) loop called `pd.concat([df, b.data])` N-1 times. See `inewave/nwlistop/modelos/arquivos/arquivoree.py`.
- **PEP 562 lazy import pattern**: `inewave/nwlistop/__init__.py` and `inewave/newave/__init__.py` replace 171 and 76 eager imports respectively with `_LAZY_IMPORTS: dict[str, str]`, `__all__ = sorted(...)`, `def __getattr__(name)` (with `globals()[name] = value` caching), and `def __dir__() -> list[str]: return __all__`.
- **`__dir__` required alongside `__getattr__`**: Without `__dir__`, `dir(inewave.nwlistop)` returns only already-cached names. Both subpackage `__init__.py` files define `def __dir__() -> list[str]: return __all__`.
- **`globals()[name] = value` caching eliminates repeat `__getattr__` calls**: After first access, the resolved class is stored directly in the module namespace so subsequent accesses bypass `__getattr__` entirely.
- **VERSIONS declaration pattern**: Handler files use `BLOCKS = [HeaderBlock, LatestBlock]` and `VERSIONS = { "version_key": [HeaderBlock, OlderBlock], ... }`. Lexicographic `<=` determines block selection. See `inewave/nwlistop/cmarg.py` and `inewave/nwlistop/pivarm.py`.
- **Series carry-forward as static mutation**: `TabelaSeriePatamarAnual._apply_series_carry_forward()` mutates the parsed dict in-place; default fill is `1`. See `tabela_serie_patamar_anual.py` lines 112-124.
- **DeprecationWarning in `__init__` for replaced classes**: `ValoresSerie` / `ValoresSeriePatamar` emit warnings at `stacklevel=2` and are not deleted. See `inewave/nwlistop/modelos/blocos/valoresserie.py`.
- **Phase-level instrumentation via monkey-patching**: `benchmarks/profile_read.py` measures per-phase timing by wrapping `TabularParser.parse_lines`, `TabelaSerieAnual._build_dataframe`, and `formata_df_meses_para_datas_nwlistop`. Originals are saved from `class.__dict__` before any patching and restored in `finally`. See `benchmarks/profile_read.py`.
- **Import benchmark isolation**: `bench_import.py` clears only `sys.modules` keys starting with `"inewave"` between iterations; cfinterface/pandas/numpy are not cleared. See `benchmarks/bench_import.py`.
- **Aggregation benchmark separates read from `valores` access**: `run_aggregation_benchmark()` reads the handler outside the timed region and times only the first `obj.valores` access per iteration, isolating `__monta_tabela()`. See `benchmarks/bench_read.py`.

### Key Decisions

- **`>=` version bound, not `==` pin**: `pyproject.toml` uses `"cfinterface>=1.9.0"` because inewave is a library.
- **Fix cfinterface bugs upstream, not in inewave**: The `_is_null()` NaT bug fix lives in the local cfinterface copy; must be upstreamed before PyPI release.
- **mypy at non-strict level**: `mypy inewave/` passes 0 errors without `--strict` on 544 source files. Strict mode deferred to epic-05 (tickets 023-024). `__getattr__` in lazy-import `__init__.py` files will need `-> Any` return annotation under strict mode.
- **No deletion of old block classes**: `ValoresSerie` / `ValoresSeriePatamar` kept with deprecation warnings; deletion deferred to a future major version.
- **Exclude `gtert.py` from TabularSection migration**: 3-level grouping (classe + serie + patamar) cannot be expressed in the 2-level base classes. See `inewave/nwlistop/modelos/gtert.py`.
- **`nwlistcf/__init__.py` excluded from lazy import conversion**: Only 5 imports; overhead is negligible. Only nwlistop (171 imports) and newave (76 imports) were converted.
- **`inewave/__init__.py` left unchanged**: The `from . import nwlistop` statement triggers the subpackage `__init__.py` but does not load handler classes; `__getattr__` in the subpackage handles deferred loading.
- **No pytest-benchmark or asv**: Benchmark suite uses only stdlib. Not integrated into pytest. Manual regression tool run on demand.
- **Profiling before optimizing**: Ticket-019 was a hard prerequisite for 020-021. Profiling revealed `TabularParser.parse_lines` at 28-32% of nwlistop read time and `__monta_tabela` as O(n^2) risk (invisible with single-year mock data but real at production scale).
- **Zero new VERSIONS needed**: The version audit in `version-catalog.md` confirmed no additional nwlistop or newave files require VERSIONS beyond the 5 already versioned.
- **No detect_version() helper needed**: `validate()` is inherited and sufficient. See ticket-017 findings.
- **Validate() is inherited and sufficient**: Returns `VersionMatchResult(matched, missing_types, unexpected_types, default_ratio)`. No custom implementation needed.

### Key Files

- `pyproject.toml`: Dependency floor `"cfinterface>=1.9.0"` with `[tool.uv.sources]` local override; remove override once cfinterface 1.9.0 ships to PyPI.
- `inewave/__init__.py`: Package version `"1.13.0"`; Hatchling reads this as canonical version.
- `inewave/nwlistop/__init__.py`: Lazy import module — `_LAZY_IMPORTS` dict (171 entries), `__all__`, `__getattr__`, `__dir__`.
- `inewave/newave/__init__.py`: Lazy import module — `_LAZY_IMPORTS` dict (76 entries), same pattern.
- `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`: Base class for `ValoresSerie` family (77+ subclasses). 113 LOC. Defines `COLUMNS`, `_build_dataframe()`, `_tidy_to_wide()`.
- `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py`: Base class for `ValoresSeriePatamar` family (87+ subclasses). 156 LOC. Adds series carry-forward.
- `inewave/nwlistop/modelos/arquivos/arquivoree.py`: Reference archive base with collect-then-concat `__monta_tabela()` and isinstance dual-type guard.
- `inewave/nwlistop/cmarg.py`: Reference handler with VERSIONS dictionary.
- `inewave/nwlistop/pivarm.py`: Reference handler with format-variant VERSIONS using `format="E"`.
- `inewave/newave/avl_cortesfpha_nwv.py`: Reference newave BlockFile with VERSIONS.
- `benchmarks/profile_read.py`: Phase-level profiling script with monkey-patch instrumentation. Produces `benchmarks/profile_report.md`.
- `benchmarks/profile_report.md`: Committed baseline — import times, per-phase breakdown for 6 file types, key findings, and recommendations.
- `benchmarks/bench_read.py`: Reusable read and aggregation benchmark functions with `BenchmarkResult` dataclass.
- `benchmarks/bench_import.py`: Reusable import benchmark functions with inewave-only `sys.modules` isolation.
- `benchmarks/run_benchmarks.py`: Entry point (`--iterations N`, default 10), produces `benchmarks/benchmark_results.md` with optional delta % column.
- `benchmarks/benchmark_results.md`: Current baseline for regression detection.
- `tests/mocks/mock_open.py`: Project mock-open helper supporting `seek()` and `tell()`. Resets stream on every call via `reset_data` side-effect. Required for all benchmark read operations.
- `plans/inewave-quality-performance/version-catalog.md`: Comprehensive 417-line audit of versioned/unversioned files. Documents lexicographic key convention.
- `/home/rogerio/git/cfinterface/cfinterface/_utils/__init__.py`: Contains the NaT-safe `_is_null()` fix; must be upstreamed.

### Conventions

- **Import ordering**: `cfinterface` imports first, then `inewave` local imports, then `typing` last. `StorageType` import belongs in the cfinterface group.
- **No DeprecationWarning suppression**: Warnings must be eliminated at the source, not filtered via `filterwarnings` in `conftest.py`.
- **`__slots__ = []` on every block subclass**: Mandatory to preserve memory layout across all nwlistop model files.
- **VERSIONS key naming**: Bare NEWAVE version strings (`"27"`, `"28"`, `"29.4.1"`). No `"v"` prefix. Lexicographic comparison — do not "fix" to semantic versioning.
- **read(version=...) convention**: `handler.read(path, version="27")` instead of deprecated `set_version()`.
- **validate() convention**: `handler.validate(version=known_version)` returns `VersionMatchResult`.
- **Test baseline is 1134 tests**: As of epic-03 completion. Plan documents "430+" which is stale.
- **`_LAZY_IMPORTS` dict key ordering**: Deprecated entries at top (matching original `# Deprecated` comment block), then active handlers in original import order. `__all__ = sorted(...)` for deterministic `dir()`.
- **Module names must be extracted from existing imports, not guessed**: `CVRHQs` -> `c_v_rhq_s`; `Def` -> `deficit`; `Re` (newave) -> `re` (shadows stdlib). See `inewave/nwlistop/__init__.py`.
- **Benchmark handler/mock loading always via `importlib.import_module`**: Never import inewave at benchmark module top-level; all handler and mock imports happen inside benchmark functions.
- **Plan for a cleanup pass after batch migrations**: Batch migrations introduce AI bloat. Explicitly budget a code-simplifier pass after each batch ticket group.

### Warnings

- **cfinterface 1.9.0 identity-based removal is a silent breaking change**: `_index_of()` uses `is` not `==`. `remove()` / `add_before()` / `add_after()` with objects from a different container instance raise `ValueError`. Search `tests/` for `\.data\.remove(` before any epic using those methods.
- **cfinterface 1.9.0 NaT bug not yet on PyPI**: `math.isnan(pandas.NaT)` raises `TypeError`. Fix in local cfinterface copy only.
- **`[tool.uv.sources]` override must be removed before PyPI release**: Will break installs for anyone without `/home/rogerio/git/cfinterface`.
- **cfinterface minor version bumps may be breaking**: The equality-to-identity change in `_index_of()` was not backward compatible despite being a minor bump. Treat all minor bumps as potentially breaking for `remove()` / `add_before()` / `add_after()` code.
- **mypy strict requires `ClassVar` on `COLUMNS`**: Current `COLUMNS: List[ColumnDef] = []` on both base classes will need `ClassVar[List[ColumnDef]]`. Plan for this in tickets 023-024.
- **`__getattr__` in lazy `__init__.py` needs `-> Any` under mypy strict**: The current untyped `def __getattr__(name: str):` will produce a strict-mode error. See `inewave/nwlistop/__init__.py` line 182.
- **`__monta_tabela` aggregation time is zero with single-year mock data**: The O(n^2) fix from ticket-020 is invisible in benchmark results because all mocks contain 1 year block. The improvement only manifests on real NEWAVE output files with 20+ blocks.
- **`Pmo` uses a different DataFrame path**: Not `TabularParser` but `DataFrame.apply` + `DataFrame.melt` in `converte_tabela_em_df()`. Phase profiling wrappers produce 0 for Pmo; use cProfile output instead. See `inewave/newave/modelos/pmo.py`.
- **Lexicographic version key comparison is counterintuitive**: `"28.12"` sorts before `"28.2"`. Do not "fix" to semantic versioning.
- **Import time measurements are highly variable**: OS page-cache effects cause wide variance across runs. The headline 24% improvement figure comes from subpackage cold-load time, not `import inewave` total time.
- **Unconfirmed version candidates need real-world testing**: dger, pmo, patamar, sistema may have graceful degradation for older NEWAVE versions; confirmation requires parsing actual files from pre-v28 versions.
- **Snapshot LOC before batch migrations**: Plan assumed ">30% LOC reduction" but no pre-migration baseline was recorded. Always capture `wc -l` totals before starting a batch migration epic.
