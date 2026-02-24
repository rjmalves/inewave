# Epic 07: Documentation

## Goals

1. Create a migration guide and changelog entry for downstream users upgrading to inewave v1.13+
2. Update the tutorial and versioning example to use the new `read(version=...)` API
3. Add a benchmarks README documenting the performance suite and v1.13.0 characteristics

## Scope

- Migration guide document (`MIGRATION.md` at repo root)
- CHANGELOG.md v1.13.0 entry
- Tutorial and example update for version-aware read API
- Benchmarks README (`benchmarks/README.md`)

## Scope Changes from Refinement

- **[MERGE] ticket-032 into ticket-031**: Codebase investigation revealed that the sphinx autodoc RST pages auto-generate from class docstrings which are already accurate. The only documentation updates needed (tutorial, example, changelog) fit naturally into the migration guide ticket. ticket-032 has been marked as `[REMOVED]` with an audit trail.

## Tickets

| Ticket     | Title                                                  | Effort   | Status  |
| ---------- | ------------------------------------------------------ | -------- | ------- |
| ticket-031 | Write migration guide and update changelog for v1.13.0 | 2 points | pending |
| ticket-032 | ~~Update API documentation and docstrings~~ (REMOVED)  | --       | removed |
| ticket-033 | Add performance benchmarks to documentation            | 1 point  | pending |

## Dependencies

- **Blocked By**: All epics 01-06 (completed)
- **Blocks**: None
