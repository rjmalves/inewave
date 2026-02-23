# ticket-024 Fix mypy strict mode errors in nwlistop module

## Context

### Background

After ticket-023 establishes mypy strict mode for the newave module and creates the `[tool.mypy]` configuration in `pyproject.toml`, the nwlistop module needs the same treatment. The nwlistop module is the largest subpackage (370 Python files) but produces significantly fewer strict-mode errors than newave because the TabularSection migration in Epic 02 already added typed base classes (`TabelaSerieAnual`, `TabelaSeriePatamarAnual`) that reduced untyped code. Additionally, nwlistop handler files are much simpler than newave handlers -- most are a single class inheriting from an archive base with a `BLOCKS` declaration and no additional methods.

### Relation to Epic

This is the second mypy strict ticket in Epic 05. It extends the strict mode configuration from ticket-023 to cover `inewave.nwlistop.*` and `inewave.nwlistcf.*` (the two remaining subpackages). After this ticket, the entire `inewave/` package passes mypy strict mode.

### Current State

Running `mypy inewave/nwlistop/ --strict` produces **287 errors in 69 files** (checked 370 source files). The error breakdown by category is:

| Error Code        | Count | Description                                  |
| ----------------- | ----- | -------------------------------------------- |
| `no-untyped-def`  | 169   | Missing return type or parameter annotations |
| `no-any-return`   | 50    | Returning `Any` from typed function          |
| `type-arg`        | 49    | Missing type parameters (bare `IO`)          |
| `unused-ignore`   | 14    | Stale `# type: ignore` comments              |
| `no-untyped-call` | 4     | Calling untyped function from typed context  |
| `attr-defined`    | 1     | Attribute access on wrong type               |

The nwlistop check also pulls in cross-module dependencies. Errors in `inewave/nwlistcf/` files (78 errors in 12 files) appear because nwlistop shares patterns with nwlistcf. The `inewave/nwlistop/__init__.py` line 182 has `def __getattr__(name: str):` missing the `-> Any` return annotation, same pattern as the newave fix in ticket-023.

The highest-error files are:

- `inewave/nwlistop/modelos/nwlistopdat.py` -- 22 errors (the most complex Section subclass in nwlistop, with `read_op1/op2/op4` methods and nested `IO` usage)
- `inewave/nwlistop/nwlistopdat.py` -- 15 errors (handler with setter methods)
- `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py` -- 11 errors
- `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py` -- 9 errors
- `inewave/nwlistop/modelos/blocos/valoresserie.py` -- 9 errors (deprecated)
- `inewave/nwlistop/modelos/blocos/valoresseriepatamar.py` -- 9 errors (deprecated)
- `inewave/nwlistop/modelos/blocos/valoresclassetermicaseriepatamar.py` -- 9 errors
- 9x `medias*.py` model files -- 5 errors each (Section subclasses)
- 7x header block files (ree.py, submercado.py, usina.py, restricao.py, parsubmercados.py, estacaobombeamento.py) -- 5 errors each
- 13 archive base files -- 2-3 errors each (mostly `__init__` args)

301 of the 370 nwlistop Python files produce **0 strict-mode errors**. These are the migrated model subclass files that inherit from `TabelaSerieAnual` or `TabelaSeriePatamarAnual` and define only `COLUMNS`.

## Specification

### Requirements

1. Extend the mypy strict configuration in `pyproject.toml` to cover `inewave.nwlistop.*`, `inewave.nwlistcf.*`, and any remaining uncovered modules (`inewave._utils.*`, `inewave.libs.*`, `inewave.config`)
2. Fix ALL mypy strict errors so that `mypy inewave/ --strict` reports 0 errors across the entire package
3. The lazy `__init__.py` `__getattr__` function in nwlistop must be annotated `-> Any`
4. All 1134 existing tests must continue to pass
5. No behavioral changes -- annotations only

### Configuration Additions

Extend the `[tool.mypy]` section from ticket-023:

```toml
[[tool.mypy.overrides]]
module = "inewave.nwlistop.*"
strict = true
warn_return_any = false

[[tool.mypy.overrides]]
module = "inewave.nwlistop"
strict = true
warn_return_any = false

[[tool.mypy.overrides]]
module = "inewave.nwlistcf.*"
strict = true
warn_return_any = false

[[tool.mypy.overrides]]
module = "inewave._utils.*"
strict = true
warn_return_any = false

[[tool.mypy.overrides]]
module = "inewave.libs.*"
strict = true
warn_return_any = false
```

The `warn_return_any = false` rationale is the same as ticket-023: cfinterface `Block.data` and `Section.data` are `Any`-typed.

### Annotation Patterns

The same patterns from ticket-023 apply. The nwlistop-specific patterns are:

**Header block classes** (REE, Submercado, Usina, Restricao, ParSubmercados, EstacaoBombeamento): Same Section/Block subclass pattern:

```python
def __init__(self, previous: Optional[Any] = None, next: Optional[Any] = None, data: Optional[Any] = None) -> None:
def read(self, file: IO[str], *args: Any, **kwargs: Any) -> None:
```

**Archive base classes** (13 files in `modelos/arquivos/`): Add `data` parameter type to `__init__`:

```python
def __init__(self, data: Any = ...) -> None:
```

**`TabelaSerieAnual` and `TabelaSeriePatamarAnual`**: Fix `IO` to `IO[str]`, add `Any` types to `*args, **kwargs`, ensure `COLUMNS` class variable is properly typed.

**Deprecated block classes** (`ValoresSerie`, `ValoresSeriePatamar`, `ValoresClasseTermicaSeriePatamar`): Same annotation pattern. These are kept with deprecation warnings (learnings: "No deletion of old block classes").

**Medias model files** (9 files): Section subclass pattern with CSV reading.

**`nwlistopdat.py` model**: The most complex file. Has private methods like `__read_op1`, `__read_op2`, `__read_op4`, `__write_op1`, etc. Each needs return type `-> None` and `IO[str]` parameterization.

### Inputs/Props

No new inputs. This is purely an annotation task.

### Outputs/Behavior

Zero behavioral changes. The only modifications are:

- Type annotations added to function signatures
- `pyproject.toml` gains additional mypy override sections
- Stale `# type: ignore` comments removed where mypy flags `unused-ignore`

### Error Handling

No changes to error handling. This ticket adds annotations only.

## Acceptance Criteria

- [ ] Given the entire inewave package, when running `mypy inewave/ --strict`, then 0 errors are reported
- [ ] Given `pyproject.toml`, when inspecting it, then it contains mypy strict overrides for `inewave.nwlistop.*`, `inewave.nwlistcf.*`, `inewave._utils.*`, and `inewave.libs.*`
- [ ] Given `inewave/nwlistop/__init__.py`, when inspecting line 182, then `__getattr__` has return type annotation `-> Any`
- [ ] Given the full test suite, when running `pytest`, then all 1134 tests pass
- [ ] Given the codebase, when running `ruff check inewave/`, then 0 errors are reported
- [ ] Given the nwlistop header block files (ree.py, submercado.py, usina.py, restricao.py, parsubmercados.py, estacaobombeamento.py), when inspecting `__init__` and `read` methods, then all parameters have type annotations and `IO` is parameterized
- [ ] Given the nwlistop archive base files (13 files in `modelos/arquivos/`), when inspecting `__init__`, then the `data` parameter has a type annotation
- [ ] Given the nwlistop model files, when searching for stale `# type: ignore` comments, then the 14 `unused-ignore` instances have been removed

## Implementation Guide

### Suggested Approach

1. **Extend `pyproject.toml`** with mypy overrides for nwlistop, nwlistcf, \_utils, and libs modules. Run `mypy inewave/ --strict` to verify the new error count (should show nwlistop + nwlistcf + \_utils + libs errors, with newave at 0 from ticket-023).

2. **Fix `inewave/nwlistop/__init__.py`** (1 error): Add `-> Any` to `__getattr__` and import `Any` from `typing`.

3. **Fix header block files** (6 files, 5 errors each = 30 errors):
   - `inewave/nwlistop/modelos/blocos/ree.py`
   - `inewave/nwlistop/modelos/blocos/submercado.py`
   - `inewave/nwlistop/modelos/blocos/usina.py`
   - `inewave/nwlistop/modelos/blocos/restricao.py`
   - `inewave/nwlistop/modelos/blocos/parsubmercados.py`
   - `inewave/nwlistop/modelos/blocos/estacaobombeamento.py`

4. **Fix the new base classes** (2 files, 9-11 errors each):
   - `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`
   - `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py`

5. **Fix deprecated block classes** (3 files, 9 errors each):
   - `inewave/nwlistop/modelos/blocos/valoresserie.py`
   - `inewave/nwlistop/modelos/blocos/valoresseriepatamar.py`
   - `inewave/nwlistop/modelos/blocos/valoresclassetermicaseriepatamar.py`

6. **Fix archive base classes** (13 files in `modelos/arquivos/`, 2-3 errors each):
   - Add type annotation to `__init__` `data` parameter

7. **Fix medias model files** (9 files, 5 errors each):
   - `mediasree.py`, `mediassin.py`, `mediasmerc.py`, `mediasusih.py`, `mediasusit.py`, `mediasusie.py`, `mediasrep.py`, `mediasrhq.py`, `mediasrhv.py`

8. **Fix `nwlistopdat.py`** model (22 errors) and handler (15 errors).

9. **Fix nwlistcf files** (78 errors across 12 files) and `inewave/_utils/formatacao.py`.

10. **Fix `inewave/libs/`** files if any errors remain.

11. **Remove stale `# type: ignore` comments** flagged as `unused-ignore`.

12. **Run `mypy inewave/ --strict`** and iterate until 0 errors.

13. **Run `pytest`** to verify all 1134 tests pass.

### Key Files to Modify

- `pyproject.toml` -- extend `[tool.mypy]` overrides
- `inewave/nwlistop/__init__.py` -- `__getattr__` return type
- `inewave/nwlistop/modelos/nwlistopdat.py` -- 22 errors
- `inewave/nwlistop/nwlistopdat.py` -- 15 errors
- `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py` -- 11 errors
- `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py` -- 9 errors
- `inewave/nwlistop/modelos/blocos/valoresserie.py` -- 9 errors
- `inewave/nwlistop/modelos/blocos/valoresseriepatamar.py` -- 9 errors
- `inewave/nwlistop/modelos/blocos/valoresclassetermicaseriepatamar.py` -- 9 errors
- 6 header block files in `inewave/nwlistop/modelos/blocos/` -- 5 errors each
- 13 archive base files in `inewave/nwlistop/modelos/arquivos/` -- 2-3 errors each
- 9 medias model files in `inewave/nwlistop/modelos/` -- 5 errors each
- `inewave/nwlistcf/modelos/arquivos.py`, `caso.py`, `nwlistcfrel.py`, `nwlistcfdat.py`, `estados.py`
- `inewave/nwlistcf/arquivos.py`, `caso.py`, `nwlistcfdat.py`, `nwlistcfrel.py`, `estados.py`
- `inewave/_utils/formatacao.py`
- `inewave/libs/usinas_hidreletricas.py`, `restricoes.py`, `eolica.py`

### Patterns to Follow

- Follow the exact same annotation patterns established in ticket-023 for newave
- For `TabelaSerieAnual` and `TabelaSeriePatamarAnual`, add `COLUMNS: ClassVar[List[ColumnDef]] = []` only if mypy requires it (the learnings note this as a potential need)
- For archive base `__init__` data parameter: use `data: Any = ...` to match `BlockFile.__init__` signature
- For `__monta_tabela` return type: use `-> Optional[pd.DataFrame]` since it can return `None`
- Deprecated classes get the same annotations -- they are not deleted (learnings: "No deletion of old block classes")

### Pitfalls to Avoid

- **Do NOT remove `# type: ignore` comments on `import pandas as pd` and `import numpy as np`** unless mypy confirms they are `unused-ignore`. Some environments may lack stubs for these packages. Only remove those flagged by mypy.
- **The `gtert.py` model** has `# type: ignore` on the import line and on `DATA_LINE` construction. These may be legitimate ignores due to mixed `List[Field]` + list comprehension types. Check each one individually.
- **The `nwlistcf` module** errors are pulled into the nwlistop check via cross-module imports. Fix nwlistcf errors as part of this ticket, not as a separate effort.
- **301 nwlistop files have 0 errors** -- do not touch them. They are the migrated model subclasses that already have proper typing via inheritance.
- **Do NOT change the `warn_return_any` setting** to `true` for nwlistop. Same rationale as newave.

## Testing Requirements

### Unit Tests

No new tests. Run the existing 1134 tests to confirm no regressions.

### Integration Tests

Run `mypy inewave/ --strict` as part of the verification step. The entire package must report 0 errors.

### E2E Tests (if applicable)

Not applicable.

## Dependencies

- **Blocked By**: ticket-023 (mypy config and newave patterns must be established first)
- **Blocks**: ticket-026 (type: ignore cleanup depends on strict mode being active)

## Effort Estimate

**Points**: 3
**Confidence**: High -- only 287 nwlistop errors plus ~78 nwlistcf errors. Most are mechanical. The nwlistop check is much smaller than newave because the TabularSection migration already added typed base classes. The patterns are identical to those established in ticket-023.
