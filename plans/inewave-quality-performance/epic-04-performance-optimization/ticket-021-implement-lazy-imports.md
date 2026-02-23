# ticket-021 Implement lazy imports for nwlistop module

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Reduce the import time of `import inewave` by implementing lazy imports for the nwlistop module, which has 150+ submodules. Currently `inewave/__init__.py` eagerly imports all three major subpackages. If a user only needs newave files, they still pay the cost of importing 150+ nwlistop handlers. Lazy imports defer this cost until the specific handler is actually used.

## Anticipated Scope

- **Files likely to be modified**: `inewave/__init__.py`, `inewave/nwlistop/__init__.py`, possibly `inewave/newave/__init__.py`
- **Key decisions needed**: Whether to use `__getattr__` lazy import pattern (Python 3.7+) or `importlib.util.LazyLoader`; whether to make all three modules lazy or only nwlistop
- **Open questions**:
  - What is the current import time for `import inewave`? Is it actually a problem?
  - Do downstream consumers (sintetizador-newave) import specific handlers or the top-level package?
  - Will lazy imports break any existing `from inewave.nwlistop import *` patterns?

## Dependencies

- **Blocked By**: ticket-019
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
