# Per-Epic Learnings: Epic 05 — Quality and Type Safety

**Epic directory**: `plans/inewave-quality-performance/epic-05-quality-and-type-safety/`
**Tickets**: 023, 024, 025, 026
**Date extracted**: 2026-02-23

---

## Patterns Established

- **`IO[Any]` over `IO[str]` for read/write overrides**: All Section and Block subclasses in inewave use `IO[Any]` for the `file` parameter, not `IO[str]`. Using `IO[str]` triggers 193+ errors because cfinterface's `Line.write()` returns `Union[str, bytes]`, making the underlying IO type ambiguous. See `inewave/newave/modelos/dger.py` lines 35, 38 and all other read/write method overrides.
- **`# type: ignore[override]` on all read/write subclass methods**: cfinterface base classes define `read(self, file: IO, ...) -> bool` but inewave subclasses return `-> None` and use `IO[Any]`. The override incompatibility is inherent to the library boundary. 418 instances follow this pattern. See `inewave/newave/modelos/dger.py` lines 35, 84, 129, etc.
- **`Optional[Any]` for cfinterface `__init__` parameters**: All `__init__` overrides for Section/Block subclasses use `def __init__(self, previous: Optional[Any] = None, next: Optional[Any] = None, data: Optional[Any] = None) -> None:`. This matches the cfinterface parent signature. See `inewave/newave/modelos/dger.py` and all model files.
- **`-> Any` on `__getattr__` in lazy import modules**: Both lazy `__init__.py` files require `-> Any` because they dynamically import and return arbitrary handler classes. See `inewave/newave/__init__.py` line 88 and `inewave/nwlistop/__init__.py` line 183.
- **Per-module mypy overrides in `pyproject.toml`**: Each subpackage gets its own `[[tool.mypy.overrides]]` section with `strict = true` and `warn_return_any = false`. This allows gradual adoption and avoids collateral noise from cfinterface's `Any`-typed data fields. See `pyproject.toml` under `[tool.mypy]`.
- **`_DATA_BLOCK_TYPES` tuple as class variable for archive configuration**: Both `_ArquivoSerieBase` and `_ArquivoSeriePatamarBase` declare `_DATA_BLOCK_TYPES: tuple[type, ...] = (...)` as class variables. Subclasses override this single attribute to change isinstance dispatch without touching any methods. See `inewave/nwlistop/modelos/arquivos/_base_serie.py` line 20 and `arquivoclassetermicasubmercadopatamar.py` lines 23-26.
- **Two distinct base classes for series vs series+patamar archives**: `_ArquivoSerieBase` and `_ArquivoSeriePatamarBase` are kept separate rather than merged with a flag. The data-shape difference is fundamental to the public API contract. See `inewave/nwlistop/modelos/arquivos/_base_serie.py` and `_base_serie_patamar.py`.
- **`cast(Iterable[Block], self.data)` for type narrowing in `_monta_tabela`**: `BlockFile.data` returns `Any` from cfinterface. A `cast()` at the loop boundary gives mypy enough information to type-check the loop body without suppressing anything. See `inewave/nwlistop/modelos/arquivos/_base_serie.py` line 29.
- **Specific error codes with inline explanations on all remaining ignores**: After ticket-026, every `# type: ignore` in the codebase uses a specific code (e.g., `[override]`, `[import-untyped]`, `[arg-type]`, `[union-attr]`) and includes a brief English explanation on the same line. Zero bare `# type: ignore` remain. See any file in `inewave/newave/modelos/` or `inewave/nwlistop/modelos/`.
- **`# type: ignore[import-untyped]` with explanation for pandas/numpy**: The project uses pandas >= 2.2.3 and numpy >= 2.2.1 which do NOT provide a `pandas-stubs` or `numpy-stubs` package recognized by mypy. The correct code is `[import-untyped]`, not no code. Explanation is `# no pandas-stubs package`. See `inewave/nwlistop/modelos/arquivos/_base_serie.py` line 3.

---

## Architectural Decisions

- **`warn_return_any = false` globally and per-module**: Decided NOT to enable `warn_return_any = true`. cfinterface's `Section.data` and `Block.data` are `Any`-typed, and every property that reads `self.data[N]` would produce a `no-any-return` error. This would require 528+ meaningless suppression comments. The decision is to accept `Any` propagation from the library boundary. Rejected alternative: add `-> Any` return types to every property. This was rejected because it would make public API types less informative.
- **`IO[Any]` not `IO[str]` or `IO[bytes]`**: After observing that `IO[str]` caused 193 errors in ticket-023 and `IO[bytes]` would cause the same on text files, `IO[Any]` was adopted uniformly. Rejected alternative: use `IO[str]` for text and `IO[bytes]` for binary (hidr.py, vazoes.py). This was rejected because `Line.write()` in cfinterface has a return type of `Union[str, bytes]`, making `IO[str]` incorrect at the library boundary regardless of the actual file mode.
- **Single `_HEADER_BLOCK` attribute replaced by inline `get_blocks_of_type` call**: The ticket-025 design spec proposed a `_get_header_value()` helper method on the base class. The actual implementation delegates header access directly to each subclass's property, which calls `self.data.get_blocks_of_type(HeaderType)`. This is more readable and avoids the base class needing to know about header block types. See `inewave/nwlistop/modelos/arquivos/arquivoree.py` lines 17-27.
- **`_monta_tabela` uses single-underscore (not double-underscore)**: The original `__monta_tabela` method used Python name mangling (class-specific private). The shared base class uses `_monta_tabela` with a single underscore so the method is accessible to subclasses and can be overridden if needed. This is documented in the ticket as a deliberate naming change.

---

## Files and Structures Created

- `inewave/nwlistop/modelos/arquivos/_base_serie.py`: Base class `_ArquivoSerieBase` (51 lines). Holds `__values` cache, `_monta_tabela()` with collect-then-concat, `valores` property, and `_DATA_BLOCK_TYPES` class variable defaulting to `(ValoresSerie, TabelaSerieAnual)`.
- `inewave/nwlistop/modelos/arquivos/_base_serie_patamar.py`: Base class `_ArquivoSeriePatamarBase` (59 lines). Same structure as above but `_DATA_BLOCK_TYPES` defaults to `(ValoresSeriePatamar, TabelaSeriePatamarAnual)`.
- `pyproject.toml` — `[tool.mypy]` section: 8 `[[tool.mypy.overrides]]` blocks covering every inewave subpackage. All use `strict = true` and `warn_return_any = false`.

---

## Conventions Adopted

- **All property setters annotated `-> None`**: Every `@property.setter` method in the codebase now carries an explicit `-> None` return annotation. This was the most common missing annotation in handler files.
- **Nested conversion functions annotated**: Private functions defined inside `read()` methods (e.g., `converte_tabela_em_df()` inside `pmo.py`) carry explicit return type annotations (`-> pd.DataFrame`).
- **`__slots__: list[str] = []` (lowercase generic) on all archive subclasses**: After the base class refactor, all thin archive subclasses declare `__slots__: list[str] = []` using the Python 3.9+ lowercase `list` type rather than `List`. See `inewave/nwlistop/modelos/arquivos/arquivoree.py` line 13.
- **Mypy strict scope covers all production code**: All of `inewave/newave`, `inewave/nwlistop`, `inewave/nwlistcf`, `inewave/_utils`, and `inewave/libs` are under strict mode. `benchmarks/` is excluded from mypy scope.
- **`# type: ignore[import-untyped]` for all pandas/numpy imports**: 138 instances across the codebase. The bare `# type: ignore` form was eliminated. The specific code clarifies that the ignore is due to missing stubs, not a type error in the code itself.

---

## Surprises and Deviations

- **`IO[str]` caused 193 errors, not 0**: The ticket-023 spec initially proposed using `IO[str]` for text files and `IO[bytes]` for binary files. When implemented, `IO[str]` caused 193 errors because cfinterface's `Line.write()` returns `Union[str, bytes]`. The actual implementation uses `IO[Any]` uniformly. The deviation is documented inline in all 418 `[override]` comment lines.
- **pandas/numpy imports still need `# type: ignore[import-untyped]`**: The ticket-026 spec predicted that all 149 `import pandas as pd # type: ignore` and 40 `import numpy as np # type: ignore` would become `unused-ignore` because "modern versions ship with `py.typed` markers." In practice, pandas 2.2.3 and numpy 2.2.1 do NOT provide a `pandas-stubs` or `numpy-stubs` package that mypy resolves. The ignores are still needed — but now correctly narrowed to `[import-untyped]`. Final count: 138 `[import-untyped]` (not 0).
- **`_get_header_value()` helper was not implemented**: The ticket-025 design spec described a `_get_header_value()` helper method on both base classes. The actual implementation omits this helper; each subclass's property accesses `self.data.get_blocks_of_type(HeaderType)` directly. This is simpler and does not require the base class to reference specific header types. See `inewave/nwlistop/modelos/arquivos/arquivoree.py`.
- **Archive line reduction was 53.5%, exceeding the 30% target**: The ticket required "at least 30% less than the current ~830 lines." The actual result was 388 total lines across all 13 archive files + 110 lines for both base files = 498 lines total, down from ~830. Non-blank line reduction was reported as 53.5% (830 -> 386 non-blank lines).
- **`# type: ignore[arg-type]` count is 16, not 14**: The ticket dispatch summary stated "14 [arg-type]" but the actual count is 16: 14 in newave model files (numpy array passed to dict expecting `List[str]`) plus 2 in `tabela_serie_anual.py` and `tabela_serie_patamar_anual.py` (int literal assigned to pandas Series column). See `inewave/newave/modelos/patamar.py` lines 109, 212, 347, 497 and `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py` line 95.

---

## Recommendations for Future Epics

- **Before adding new Section/Block subclasses, copy the `dger.py` method signature template**: Every new Section subclass needs `__init__(self, previous: Optional[Any] = None, next: Optional[Any] = None, data: Optional[Any] = None) -> None:`, `read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]`, and `write(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]`. Treat `inewave/newave/modelos/dger.py` as the canonical pattern file.
- **When adding a new nwlistop archive, inherit from `_ArquivoSerieBase` or `_ArquivoSeriePatamarBase`**: See `inewave/nwlistop/modelos/arquivos/arquivoree.py` for the canonical thin-subclass pattern. Override `_DATA_BLOCK_TYPES` only if using a non-standard block type (as in `arquivoclassetermicasubmercadopatamar.py`).
- **Do not upgrade cfinterface minor versions without auditing `IO[Any]` compatibility**: The `IO[Any]` convention exists because of cfinterface's `Line.write()` return type. If cfinterface is updated to return `str` only, the `[override]` ignores may become unnecessary. Run `mypy inewave/ --strict` after any cfinterface upgrade.
- **Strict mypy is now a CI gate**: Once CI is configured to run `mypy inewave/ --strict`, any new file that omits return types or uses bare `IO` will fail CI. Ensure all future specialists are aware of the `IO[Any]` + `[override]` annotation pattern before implementing new model files.
- **Benchmark files are outside mypy strict scope**: `benchmarks/` is not covered by any `[[tool.mypy.overrides]]` block. If benchmark files need type checking, add a separate override. Currently they carry their own `# type: ignore` comments that are not validated by mypy strict.
