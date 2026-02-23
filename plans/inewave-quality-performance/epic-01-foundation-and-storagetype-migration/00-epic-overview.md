# Epic 01: Foundation and StorageType Migration

## Goals

1. Bump the cfinterface dependency from `>= 1.8.0` to `>= 1.9.0` in `pyproject.toml`
2. Replace all 16 `STORAGE = "BINARY"` string literals in `inewave/newave/` with `StorageType.BINARY`
3. Add the `from cfinterface.storage import StorageType` import to all affected files
4. Verify all existing tests pass after the migration
5. Bump the inewave version to signal the new dependency

## Scope

This epic is limited to:

- `pyproject.toml` (dependency version bump, inewave version bump)
- `inewave/__init__.py` (version bump)
- 16 files in `inewave/newave/` that use `STORAGE = "BINARY"`

No nwlistop files are affected (they use BlockFile, which defaults to TEXT and has no explicit STORAGE attribute).

## Affected Files

All 16 files using `STORAGE = "BINARY"`:

1. `inewave/newave/cortes.py`
2. `inewave/newave/cortesh.py`
3. `inewave/newave/enavazb.py`
4. `inewave/newave/enavazf.py`
5. `inewave/newave/energiab.py`
6. `inewave/newave/energiaf.py`
7. `inewave/newave/energias.py`
8. `inewave/newave/engnat.py`
9. `inewave/newave/forward.py`
10. `inewave/newave/forwarh.py`
11. `inewave/newave/hidr.py`
12. `inewave/newave/vazaob.py`
13. `inewave/newave/vazaof.py`
14. `inewave/newave/vazaos.py`
15. `inewave/newave/vazinat.py`
16. `inewave/newave/vazoes.py`

## Tickets

| Ticket     | Title                                                         | Effort   |
| ---------- | ------------------------------------------------------------- | -------- |
| ticket-001 | Bump cfinterface dependency to >= 1.9.0                       | 1 point  |
| ticket-002 | Migrate STORAGE string literals to StorageType enum in newave | 2 points |
| ticket-003 | Run full test suite and fix any regressions                   | 1 point  |

## Dependencies

- Requires cfinterface v1.9.0 to be published/installable
- No dependencies on other epics

## Success Criteria

- `grep -r 'STORAGE = "' inewave/` returns zero results
- All 430+ tests pass
- `ruff check` and `mypy` pass
- cfinterface deprecation warnings are eliminated
