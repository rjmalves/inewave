# ticket-023 Enable mypy strict mode and fix newave module errors

## Context

### Background

All four prior epics are complete. The codebase passes `mypy inewave/` at non-strict level with 0 errors across 544 source files. However, under `--strict` mode, the `inewave/newave/` module produces **2892 errors in 124 files** (checked 150 source files). The newave module is the most important module because it handles NEWAVE input files that downstream code depends on for correct configuration parsing.

### Relation to Epic

Epic 05 (Quality and Type Safety) aims to bring the entire codebase under mypy strict mode. This ticket tackles the newave module first because (a) it has the most errors (2892 vs 287 for nwlistop), (b) it establishes the annotation patterns that ticket-024 will follow for nwlistop, and (c) fixing newave first may resolve some cross-module errors that appear in nwlistop's check.

### Current State

Running `mypy inewave/newave/ --strict` today produces 2892 errors across 124 files. The error breakdown by category is:

| Error Code        | Count    | Description                                         |
| ----------------- | -------- | --------------------------------------------------- |
| `no-untyped-def`  | 1684     | Missing return type or parameter annotations        |
| `no-any-return`   | 528      | Returning `Any` from typed function                 |
| `type-arg`        | 447      | Missing type parameters (bare `IO`, `List`, `Dict`) |
| `no-untyped-call` | 112      | Calling untyped function from typed context         |
| `unused-ignore`   | 106      | Stale `# type: ignore` comments                     |
| `arg-type`        | 15       | Type argument mismatches                            |
| Other             | 0-2 each | Minor issues                                        |

The single largest error source is `inewave/newave/modelos/dger.py` with **1090 errors** (38% of the total). This 5360-line file defines ~90 Section subclasses for the NEWAVE general data file, each following an identical pattern:

```python
def __init__(self, previous=None, next=None, data=None) -> None:  # no-untyped-def (args)
def read(self, file: IO, *args, **kwargs):  # no-untyped-def (return), type-arg (IO)
def write(self, file: IO, *args, **kwargs):  # no-untyped-def (return), type-arg (IO)
@property
def valor(self) -> Optional[int]:
    return self.data[1]  # no-any-return
@valor.setter
def valor(self, v: int):  # no-untyped-def (setter has no return annotation)
    self.data[1] = v
```

The newave `__init__.py` at line 87 has `def __getattr__(name: str):` missing return type -- this needs `-> Any` under strict mode as documented in the learnings.

The cfinterface base classes (`Section`, `Block`) define `__init__(self, previous=None, next=None, data=None) -> None` with untyped parameters. The `read` method signature is `def read(self, file: IO, *args, **kwargs) -> bool`. Overrides in inewave must match or be compatible.

Key affected file groups:

- **Model files** (`inewave/newave/modelos/`): 74 files, overwhelmingly `dger.py` (1090), `pmo.py` (165), `cortesh.py` (130), `forwarh.py` (96), `parp.py` (89), `hidr.py` (78)
- **Handler files** (`inewave/newave/*.py`): 76 files, mostly setter return annotations and `no-any-return` from property accessors
- **Shared blocks** (`inewave/newave/modelos/blocos/`): `versaomodelo.py` (10 errors), `tabelacsv.py` (6 errors)
- **Lazy **init**** (`inewave/newave/__init__.py`): 1 error (`__getattr__` missing return type)

## Specification

### Requirements

1. Configure mypy strict mode for the newave module in `pyproject.toml` using per-module overrides
2. Fix ALL mypy strict errors in `inewave/newave/` so that `mypy inewave/newave/ --strict` reports 0 errors
3. The lazy `__init__.py` `__getattr__` function must be annotated `-> Any`
4. All 1134 existing tests must continue to pass
5. No behavioral changes -- annotations only

### Configuration Approach

Add a `[tool.mypy]` section to `pyproject.toml` with per-module strict overrides:

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = false
warn_unused_ignores = true

[[tool.mypy.overrides]]
module = "inewave.newave.*"
strict = true
warn_return_any = false  # too noisy for cfinterface's Any-typed data

[[tool.mypy.overrides]]
module = "inewave.newave"
strict = true
warn_return_any = false
```

Note: `warn_return_any = false` is necessary because cfinterface's `Section.data` and `Block.data` are `Any`-typed. Every property that reads `self.data[N]` would trigger `no-any-return`. The alternative is to add 528+ `# type: ignore[return-value]` comments, which adds no value. Instead, the `no-any-return` errors from `self.data` access are suppressed at the module level, and all other strict checks remain active.

### Annotation Patterns

For the ~90 Section subclasses in `dger.py` and similar model files, apply these mechanical fixes:

**`__init__` parameters:** Add `Optional[Any]` types matching the cfinterface parent signature:

```python
def __init__(self, previous: Optional[Any] = None, next: Optional[Any] = None, data: Optional[Any] = None) -> None:
```

**`read`/`write` methods:** Add return type and parameterize `IO`:

```python
def read(self, file: IO[str], *args: Any, **kwargs: Any) -> None:
    ...
def write(self, file: IO[str], *args: Any, **kwargs: Any) -> None:
    ...
```

Note: newave Section subclasses return `None` from `read`/`write`, not `bool`. The parent class defines `-> bool` but the convention in this codebase is to not return a value from Section overrides. Use `-> None` to match actual behavior. If cfinterface enforces `-> bool`, use `-> bool` and add explicit `return True`.

**Setter methods:** Add `-> None` return type:

```python
@valor.setter
def valor(self, v: int) -> None:
    self.data[1] = v
```

**Bare `IO`:** Replace with `IO[str]` or `IO[bytes]` as appropriate (text files use `IO[str]`).

**Bare `List`, `Dict`:** Replace with parameterized versions: `List[str]`, `Dict[str, Any]`, etc.

**Stale `# type: ignore`:** Remove the 106 `unused-ignore` comments. These are mostly on `import pandas as pd # type: ignore` and `import numpy as np # type: ignore` lines in model files.

**Nested functions:** Functions like `converte_tabela_em_df()` inside `read()` need return type annotations under strict mode. Add `-> pd.DataFrame` return types.

### Inputs/Props

No new inputs. This is purely an annotation task.

### Outputs/Behavior

Zero behavioral changes. The only modifications are:

- Type annotations added to function signatures
- `pyproject.toml` gains a `[tool.mypy]` section
- Stale `# type: ignore` comments removed where mypy flags `unused-ignore`

### Error Handling

No changes to error handling. This ticket adds annotations only.

## Acceptance Criteria

- [ ] Given the newave module, when running `mypy inewave/newave/ --strict`, then 0 errors are reported
- [ ] Given `pyproject.toml`, when inspecting it, then it contains a `[tool.mypy]` section with strict overrides for `inewave.newave.*`
- [ ] Given the `inewave/newave/__init__.py` file, when inspecting line 87, then `__getattr__` has return type annotation `-> Any`
- [ ] Given the full test suite, when running `pytest`, then all 1134 tests pass
- [ ] Given the codebase, when running `ruff check inewave/newave/`, then 0 errors are reported (no regressions)
- [ ] Given `inewave/newave/modelos/dger.py`, when inspecting any `__init__` method, then all parameters have type annotations
- [ ] Given any `read`/`write` method in newave model files, when inspecting it, then it has a return type annotation and `IO` is parameterized as `IO[str]` or `IO[bytes]`
- [ ] Given the newave model files, when searching for stale `# type: ignore` comments, then the 106 `unused-ignore` instances have been removed

## Implementation Guide

### Suggested Approach

1. **Add `[tool.mypy]` configuration** to `pyproject.toml` first. Run `mypy inewave/newave/ --strict` to establish the baseline of 2892 errors.

2. **Fix `inewave/newave/__init__.py`** (1 error): Add `-> Any` to `__getattr__` and import `Any` from `typing`.

3. **Fix `inewave/newave/modelos/dger.py`** (1090 errors -- 38% of total): This is mechanical. The file has ~90 Section subclasses with identical structure. For each:
   - Add parameter types to `__init__`
   - Add return type and `IO[str]` to `read`/`write`
   - Add `-> None` to setter methods
   - Remove stale `# type: ignore` if present

4. **Fix remaining model files** in `inewave/newave/modelos/` (pmo.py, cortesh.py, forwarh.py, parp.py, hidr.py, etc.). Same mechanical patterns.

5. **Fix shared blocks** in `inewave/newave/modelos/blocos/` (versaomodelo.py, tabelacsv.py).

6. **Fix handler files** in `inewave/newave/*.py` (76 files). These mostly need `-> None` on setter methods and `-> None` on private helper methods.

7. **Remove stale `# type: ignore` comments** flagged as `unused-ignore`.

8. **Run `mypy inewave/newave/ --strict`** and iterate until 0 errors.

9. **Run `pytest`** to verify all 1134 tests pass.

### Key Files to Modify

- `pyproject.toml` -- add `[tool.mypy]` section
- `inewave/newave/__init__.py` -- `__getattr__` return type
- `inewave/newave/modelos/dger.py` -- 1090 errors, largest single file
- `inewave/newave/modelos/pmo.py` -- 165 errors
- `inewave/newave/modelos/cortesh.py` -- 130 errors
- `inewave/newave/dger.py` -- 119 errors (the handler wrapping the model)
- `inewave/newave/modelos/forwarh.py` -- 96 errors
- `inewave/newave/modelos/parp.py` -- 89 errors
- `inewave/newave/modelos/hidr.py` -- 78 errors
- `inewave/newave/modelos/parpvaz.py` -- 66 errors
- `inewave/newave/modelos/curva.py` -- 64 errors
- `inewave/newave/modelos/modif.py` -- 58 errors
- `inewave/newave/modelos/patamar.py` -- 57 errors
- `inewave/newave/modelos/sistema.py` -- 56 errors
- `inewave/newave/modelos/parpeol.py` -- 50 errors
- `inewave/newave/arquivos.py` -- 47 errors
- All remaining files in `inewave/newave/modelos/` and `inewave/newave/`
- `inewave/newave/modelos/blocos/versaomodelo.py` -- 10 errors
- `inewave/newave/modelos/blocos/tabelacsv.py` -- 6 errors

### Patterns to Follow

- **cfinterface `__init__` override**: Use `Optional[Any]` for `previous`, `next`, `data` parameters. Import `Any` from `typing`.
- **`read`/`write` in Section subclasses**: Return `-> None` (matches actual behavior). Use `IO[str]` for text files, `IO[bytes]` for binary (hidr.py, vazoes.py).
- **Property setters**: Always `-> None`.
- **Nested conversion functions**: Add explicit `-> pd.DataFrame` return type.
- **`__slots__` typing**: `__slots__: List[str] = []` does not need `ClassVar` because it is a class-level special attribute recognized by Python.
- **Lazy `__init__.py`**: Use `-> Any` for `__getattr__` because it dynamically imports and returns arbitrary handler classes.

### Pitfalls to Avoid

- **Do NOT add `warn_return_any = true`** globally. It would produce 528+ errors from `self.data` access where cfinterface stores `Any`. This is noise, not a real type safety issue.
- **Do NOT change `Section.read` override signatures to return `bool`** unless cfinterface enforces it. Current newave convention is `-> None`.
- **Do NOT remove `# type: ignore` comments that are NOT flagged as `unused-ignore`**. Some are still needed (e.g., `import pandas as pd # type: ignore` if pandas lacks stubs in the environment). Ticket-026 handles the comprehensive cleanup.
- **Do NOT touch nwlistop or nwlistcf files** in this ticket -- those are covered by ticket-024.
- **Binary files** (`hidr.py`, `vazoes.py`) use `IO[bytes]`, not `IO[str]`.
- **The `T = TypeVar("T")` class attribute** in some handlers (e.g., `Arquivos`, `Caso`) is unused. Do not remove it in this ticket (scope creep) -- note it for a future cleanup.

## Testing Requirements

### Unit Tests

No new tests. Run the existing 1134 tests to confirm no regressions.

### Integration Tests

Run `mypy inewave/newave/ --strict` as part of the verification step.

### E2E Tests (if applicable)

Not applicable.

## Dependencies

- **Blocked By**: ticket-013 (completed -- deprecated blocks cleaned up)
- **Blocks**: ticket-024 (nwlistop strict mode depends on patterns established here)

## Effort Estimate

**Points**: 3
**Confidence**: High -- the errors are mechanical and repetitive. The largest file (dger.py) alone accounts for 38% of errors and follows a single pattern. No design decisions needed.
