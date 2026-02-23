# Epic 03: Schema Versioning for NEWAVE Version Evolution

## Goals

1. Identify all file classes that have version-dependent formats across NEWAVE releases (v27, v28, v29, v30, etc.)
2. Add `VERSIONS` dictionaries to these classes using cfinterface's `resolve_version()` API
3. Enable `read(version=...)` for version-aware file reads
4. Add `validate()` support for detecting version mismatches
5. Document the versioning strategy for downstream users

## Scope

- Survey all newave and nwlistop file handlers for version-dependent formats
- Currently only 5 files have VERSIONS (cmarg, cmargmed, pivarm, pivarmincr, avl_cortesfpha_nwv)
- Target: expand to ~10-20 additional files where format changes between NEWAVE versions are known

## Tickets (Outline)

| Ticket     | Title                                                   | Effort   |
| ---------- | ------------------------------------------------------- | -------- |
| ticket-014 | Survey and catalog version-dependent file formats       | 3 points |
| ticket-015 | Add VERSIONS dictionaries to newave SectionFile classes | 3 points |
| ticket-016 | Add VERSIONS dictionaries to nwlistop BlockFile classes | 3 points |
| ticket-017 | Add validate() integration to versioned file classes    | 2 points |
| ticket-018 | Write version-aware tests for versioned file classes    | 3 points |

## Dependencies

- **Blocked By**: Epic 02 (simplified model structure makes VERSIONS easier to add)
- **Blocks**: Epic 06 (version tests depend on VERSIONS being defined)
