# Epic 1: Packaging & CI Modernization

## Goals

Modernize the project's packaging metadata, CI/CD pipelines, and developer tooling to align with current Python ecosystem standards. This epic addresses the infrastructure layer that supports all subsequent documentation and repository polish work.

## Scope

- Update `pyproject.toml` metadata: classifiers, `py.typed` inclusion in wheel, dev dependency organization
- Restructure the CI workflow from a single sequential job into parallel independent jobs
- Migrate documentation deployment from deprecated `peaceiris/actions-gh-pages@v3` to official GitHub Pages actions
- Create a dedicated release workflow with trusted publishing and version validation
- Add pre-commit hooks for ruff and mypy

## Out of Scope

- Modifying library source code or tests
- Changing the build backend (Hatchling stays)
- Upgrading Python version requirements
- Adding new CI checks not currently running (e.g., coverage thresholds, security scanning)

## Tickets

| Ticket     | Title                                                     | Effort |
| ---------- | --------------------------------------------------------- | ------ |
| ticket-001 | Modernize pyproject.toml metadata and wheel configuration | 2      |
| ticket-002 | Restructure CI workflow into parallel jobs                | 3      |
| ticket-003 | Migrate docs deployment to official GitHub Pages actions  | 2      |
| ticket-004 | Create release workflow with trusted publishing           | 2      |
| ticket-005 | Add pre-commit hooks for ruff and mypy                    | 2      |

## Dependencies

- No dependencies on other epics. This epic must complete first as Epic 2 (Sphinx Modernization) depends on the updated CI and docs deployment pipeline.

## Acceptance Criteria

- All parallel CI jobs pass on the feature branch
- Documentation deploys successfully via official GitHub Pages actions
- Release workflow triggers correctly on tag push and publishes to PyPI
- `pre-commit run --all-files` passes with zero errors
