# ticket-002 Migrate STORAGE string literals to StorageType enum in newave

## Context

### Background

cfinterface v1.9.0 introduced `StorageType(str, Enum)` in `cfinterface/storage.py` with members `StorageType.TEXT` and `StorageType.BINARY`. The old pattern of `STORAGE = "BINARY"` as a plain string still works (backward compatible via `str` mixin hash equality), but emits a `DeprecationWarning` at file-class `__init__` time via `_ensure_storage_type()`. All 16 occurrences in inewave are in the `newave/` module and all use `"BINARY"`.

### Relation to Epic

This is the core migration ticket of Epic 01. It eliminates all deprecation warnings from the StorageType change and modernizes the codebase to use the enum.

### Current State

16 files in `inewave/newave/` contain `STORAGE = "BINARY"` as a class attribute:

| #   | File                         | Line | Parent Class |
| --- | ---------------------------- | ---- | ------------ |
| 1   | `inewave/newave/cortes.py`   | 17   | SectionFile  |
| 2   | `inewave/newave/cortesh.py`  | 17   | SectionFile  |
| 3   | `inewave/newave/enavazb.py`  | 18   | SectionFile  |
| 4   | `inewave/newave/enavazf.py`  | 18   | SectionFile  |
| 5   | `inewave/newave/energiab.py` | 17   | SectionFile  |
| 6   | `inewave/newave/energiaf.py` | 17   | SectionFile  |
| 7   | `inewave/newave/energias.py` | 17   | SectionFile  |
| 8   | `inewave/newave/engnat.py`   | 18   | SectionFile  |
| 9   | `inewave/newave/forward.py`  | 18   | SectionFile  |
| 10  | `inewave/newave/forwarh.py`  | 17   | SectionFile  |
| 11  | `inewave/newave/hidr.py`     | 19   | RegisterFile |
| 12  | `inewave/newave/vazaob.py`   | 17   | SectionFile  |
| 13  | `inewave/newave/vazaof.py`   | 17   | SectionFile  |
| 14  | `inewave/newave/vazaos.py`   | 17   | SectionFile  |
| 15  | `inewave/newave/vazinat.py`  | 17   | SectionFile  |
| 16  | `inewave/newave/vazoes.py`   | 21   | RegisterFile |

No files in nwlistop, nwlistcf, or libs use an explicit STORAGE attribute (they all inherit the default `StorageType.TEXT` from their BlockFile base class).

## Specification

### Requirements

For each of the 16 files listed above:

1. Add the import `from cfinterface.storage import StorageType` at the top of the file (after existing cfinterface imports)
2. Replace `STORAGE = "BINARY"` with `STORAGE = StorageType.BINARY`

### Inputs/Props

None -- pure refactoring.

### Outputs/Behavior

- All 16 files use `StorageType.BINARY` instead of `"BINARY"`
- All files have the `from cfinterface.storage import StorageType` import
- `grep -r 'STORAGE = "' inewave/` returns zero results
- No `DeprecationWarning` is emitted when instantiating any inewave file class

### Error Handling

Not applicable -- this is a mechanical string-to-enum replacement with no behavioral change.

## Acceptance Criteria

- [ ] Given the inewave codebase, when I run `grep -rn 'STORAGE = "' inewave/`, then zero results are returned
- [ ] Given `inewave/newave/hidr.py`, when I read it, then line 19 contains `STORAGE = StorageType.BINARY` and an import for `StorageType` exists at the top
- [ ] Given `inewave/newave/vazoes.py`, when I read it, then line 21 contains `STORAGE = StorageType.BINARY` and an import for `StorageType` exists at the top
- [ ] Given any of the 16 files, when I instantiate the file class with `warnings.catch_warnings(record=True)` active, then no `DeprecationWarning` is captured
- [ ] Given the codebase, when I run `ruff check inewave/`, then no import or formatting errors are reported for the modified files

## Implementation Guide

### Suggested Approach

This is a mechanical, repetitive change. For each of the 16 files:

1. Open the file
2. Locate the existing cfinterface imports (e.g., `from cfinterface.files.sectionfile import SectionFile`)
3. Add `from cfinterface.storage import StorageType` immediately after the cfinterface import block
4. Replace `STORAGE = "BINARY"` with `STORAGE = StorageType.BINARY`
5. Verify indentation and line length (80 char ruff limit)

Example transformation for `inewave/newave/hidr.py`:

**Before:**

```python
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.hidr import RegistroUHEHidr
from inewave.config import MESES_ABREV
import pandas as pd  # type: ignore

from typing import TypeVar, List, Optional, Union, IO

class Hidr(RegisterFile):
    T = TypeVar("T")
    REGISTERS = [RegistroUHEHidr]
    STORAGE = "BINARY"
```

**After:**

```python
from cfinterface.files.registerfile import RegisterFile
from cfinterface.storage import StorageType
from inewave.newave.modelos.hidr import RegistroUHEHidr
from inewave.config import MESES_ABREV
import pandas as pd  # type: ignore

from typing import TypeVar, List, Optional, Union, IO

class Hidr(RegisterFile):
    T = TypeVar("T")
    REGISTERS = [RegistroUHEHidr]
    STORAGE = StorageType.BINARY
```

### Key Files to Modify

All 16 files listed in the Current State section above, all under `/home/rogerio/git/inewave/inewave/newave/`.

### Patterns to Follow

- Place the `from cfinterface.storage import StorageType` import immediately after other `cfinterface` imports, before `inewave` imports (follow isort grouping: third-party, then local)
- Use `StorageType.BINARY` exactly -- not `StorageType("BINARY")`, not `StorageType["BINARY"]`

### Pitfalls to Avoid

- Do NOT change any other class attributes (SECTIONS, REGISTERS, BLOCKS, etc.)
- Do NOT modify any method bodies
- Do NOT add `StorageType` imports to files that do not have an explicit STORAGE attribute
- Respect the 80-character line length enforced by ruff

## Testing Requirements

### Unit Tests

No new tests needed. The existing tests for all 16 file types serve as regression tests.

### Integration Tests

Run the full test suite: `pytest tests/ -x` to verify no regressions.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-001 (cfinterface >= 1.9.0 must be installed)
- **Blocks**: ticket-003

## Effort Estimate

**Points**: 2
**Confidence**: High
