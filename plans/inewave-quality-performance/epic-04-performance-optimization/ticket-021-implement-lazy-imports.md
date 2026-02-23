# ticket-021 Implement lazy imports for nwlistop module

## Context

### Background

`inewave/__init__.py` eagerly imports all three subpackages:

```python
from . import newave  # noqa
from . import nwlistcf  # noqa
from . import nwlistop  # noqa
```

The `nwlistop/__init__.py` file has 171 eager import statements, each importing a handler class (e.g., `from .earmf import Earmf`). Each handler import triggers importing its model module, which imports `TabelaSerieAnual` or `TabelaSeriePatamarAnual`, which imports `TabularParser`, `Line`, various `Field` classes, and `pandas`. The `newave/__init__.py` has 76 eager imports. The `nwlistcf/__init__.py` has only 5.

This means `import inewave` pays the cost of importing all ~250 handler classes even when a user needs only one. For downstream consumers like `sintetizador-newave` that may only use a subset of handlers, this is wasteful.

### Relation to Epic

This ticket targets import-time performance, which is independent of read-time performance (addressed by ticket-020). Together they cover the two main performance bottlenecks users encounter: startup latency (import time) and operation latency (read time).

### Current State

- `inewave/__init__.py` (9 lines): Imports `newave`, `nwlistcf`, `nwlistop` eagerly.
- `inewave/nwlistop/__init__.py` (175 lines): 171 `from .xxx import Xxx` statements. All handler classes imported at module load time.
- `inewave/newave/__init__.py` (79 lines): 76 `from .xxx import Xxx` statements.
- `inewave/nwlistcf/__init__.py` (7 lines): 5 `from .xxx import Xxx` statements. Too small to optimize.
- Python version target: 3.10+. The `__getattr__` lazy import pattern (PEP 562) is available since Python 3.7.
- The `__all__` list is NOT defined in any of the `__init__.py` files. Handler classes are accessed via `from inewave.nwlistop import Earmf` or `from inewave.nwlistop.earmf import Earmf` (the latter bypasses the `__init__.py`).
- Test count baseline: 1134 tests.

## Specification

### Requirements

1. Convert `inewave/nwlistop/__init__.py` from eager imports to lazy imports using the `__getattr__` + `__all__` pattern (PEP 562).
2. Convert `inewave/newave/__init__.py` from eager imports to lazy imports using the same pattern.
3. Do NOT convert `inewave/nwlistcf/__init__.py` (only 5 imports; overhead negligible).
4. Do NOT change `inewave/__init__.py` (the `from . import newave` statement only triggers the subpackage `__init__.py`; the lazy `__getattr__` in the subpackage handles the rest).
5. All existing import patterns must continue to work:
   - `from inewave.nwlistop import Earmf` (must trigger lazy import of `earmf` module)
   - `from inewave.nwlistop.earmf import Earmf` (bypasses `__init__.py`; must still work)
   - `import inewave; inewave.nwlistop.Earmf` (must trigger lazy import via `__getattr__`)
   - `from inewave.nwlistop import *` (must import all handlers listed in `__all__`)
6. Preserve the `# Deprecated` comment section that groups deprecated handler imports.

### Inputs/Props

Not applicable (module-level change).

### Outputs/Behavior

- `import inewave` completes faster because nwlistop and newave handler modules are not loaded until accessed.
- `from inewave.nwlistop import Earmf` loads only the `earmf` module and its dependencies, not all 171 handlers.
- `dir(inewave.nwlistop)` returns all handler names (from `__all__`).
- `from inewave.nwlistop import *` still imports all handlers (but this is an explicit choice by the user).

### Error Handling

- If a user tries to import a name that does not exist in `__all__` via `from inewave.nwlistop import NonExistent`, raise `ImportError` with a clear message (this is the default behavior of `__getattr__` raising `AttributeError`, which Python converts to `ImportError` in `from ... import` context).
- The `__getattr__` function must raise `AttributeError` for unknown attribute names.

## Acceptance Criteria

- [ ] Given `inewave/nwlistop/__init__.py` has been converted, when inspecting the file, then it contains a `_LAZY_IMPORTS` dict mapping class names to module names, an `__all__` list, and a `__getattr__` function
- [ ] Given `inewave/newave/__init__.py` has been converted, when inspecting the file, then it contains the same lazy import pattern
- [ ] Given the lazy imports are in place, when running `python -c "import inewave"`, then the command succeeds without errors
- [ ] Given the lazy imports are in place, when running `python -c "from inewave.nwlistop import Earmf; print(Earmf)"`, then the output shows the Earmf class
- [ ] Given the lazy imports are in place, when running `python -c "from inewave.nwlistop.earmf import Earmf; print(Earmf)"`, then the output shows the Earmf class (direct import still works)
- [ ] Given the lazy imports are in place, when running `pytest tests/ -x -q`, then all 1134 tests pass
- [ ] Given the lazy imports are in place, when measuring import time with `python -c "import time; t=time.perf_counter(); import inewave; print(f'{time.perf_counter()-t:.3f}s')"`, then the import time is measurably lower than before (capture before/after numbers)
- [ ] Given `inewave/nwlistcf/__init__.py`, when inspecting, then it is unchanged (still eager imports)

## Implementation Guide

### Suggested Approach

1. **Build the lazy import mapping for nwlistop.** Create a dictionary `_LAZY_IMPORTS` mapping each class name to its module name. Example entries:

   ```python
   _LAZY_IMPORTS = {
       # Deprecated
       "CVRHQs": "c_v_rhq_s",
       "CVRHQ": "c_v_rhq",
       # ... all 171 entries ...
       "Earmf": "earmf",
       "Earmfm": "earmfm",
       # ...
   }
   ```

2. **Define `__all__`** as the sorted list of all keys from `_LAZY_IMPORTS`.

3. **Implement `__getattr__`:**

   ```python
   def __getattr__(name: str):
       if name in _LAZY_IMPORTS:
           module = importlib.import_module(
               f".{_LAZY_IMPORTS[name]}", __name__
           )
           value = getattr(module, name)
           globals()[name] = value  # cache for subsequent access
           return value
       raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
   ```

4. **Add `import importlib` at the top** of the file.

5. **Remove all `from .xxx import Xxx` statements.** Replace them with the `_LAZY_IMPORTS` dict. Preserve the `# Deprecated` and `# Inclui os membros` comments as section markers within the dict for readability.

6. **Repeat for `inewave/newave/__init__.py`** with the same pattern.

7. **Measure import time before and after.** Run this one-liner before making changes and after:
   ```bash
   python -c "import time; t=time.perf_counter(); import inewave; print(f'{time.perf_counter()-t:.3f}s')"
   ```

### Key Files to Modify

- `inewave/nwlistop/__init__.py` (complete rewrite: 175 lines of imports -> ~200 lines with dict + **getattr**)
- `inewave/newave/__init__.py` (complete rewrite: 79 lines of imports -> ~100 lines with dict + **getattr**)

### Patterns to Follow

The `__getattr__` lazy module pattern is well-established in the Python ecosystem. Reference implementations:

- [PEP 562](https://peps.python.org/pep-0562/)
- NumPy uses this pattern in `numpy/__init__.py`
- The pattern caches the imported value in `globals()` so `__getattr__` is only called once per name.

### Pitfalls to Avoid

- Do NOT use `importlib.util.LazyLoader`; it is more complex and less widely adopted. The `__getattr__` pattern is simpler and sufficient.
- Do NOT forget `globals()[name] = value` in `__getattr__`. Without caching, every attribute access re-imports the module.
- Do NOT change `inewave/__init__.py`. The `from . import nwlistop` statement triggers the subpackage `__init__.py` but does NOT import handler classes (those are deferred to `__getattr__`).
- Do NOT break `from inewave.nwlistop import *`. This requires `__all__` to be defined.
- Watch for handler classes whose module name differs from the lowercase class name. For example:
  - `CVRHQs` is in module `c_v_rhq_s`
  - `CVRHQ` is in module `c_v_rhq`
  - `Def` (deficit) is in module `deficit` (not `def`, which is a keyword)
  - `BID` is in module `bid`
  - `GEE` is in module `gee`
  - `Re` is in module `re` (but this is `inewave.newave.re`, not the stdlib `re`)
    Build the mapping by extracting from the existing import statements; do not guess module names.
- Do NOT remove the `Nwlistopdat` import from the nwlistop mapping. It is a valid handler.
- Ensure the `# noqa` comments are removed since the import statements are gone.

## Testing Requirements

### Unit Tests

No new unit tests needed. The existing 1134 tests exercise all handler imports through their test files.

### Integration Tests

- Run `pytest tests/ -x -q` and verify all 1134 tests pass.
- Verify `python -c "from inewave.nwlistop import Earmf, Cmarg, Gtert"` works.
- Verify `python -c "from inewave.newave import Pmo, Hidr, Dger"` works.
- Verify `python -c "import inewave; print(dir(inewave.nwlistop))"` includes all handler names.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-019 (profiling confirms import time is worth optimizing)
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High
