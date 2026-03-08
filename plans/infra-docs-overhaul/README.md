# Infrastructure, CI/CD & Documentation Overhaul

Modernize inewave's packaging metadata, CI/CD pipelines, documentation infrastructure, and repository files.

## Tech Stack

- Python 3.10+ / Hatchling / uv
- GitHub Actions (CI/CD)
- Sphinx + Furo (documentation)
- ruff + mypy + pre-commit (developer tooling)

## Epics

| Epic    | Name                            | Tickets | Detail Level |
| ------- | ------------------------------- | ------- | ------------ |
| epic-01 | Packaging & CI Modernization    | 5       | Detailed     |
| epic-02 | Sphinx Modernization            | 2       | Detailed     |
| epic-03 | Documentation Content Expansion | 5       | Outline      |
| epic-04 | Repository Polish               | 4       | Outline      |

## Progress

| Ticket     | Title                                                     | Epic    | Status    | Detail Level | Readiness | Quality | Badge     |
| ---------- | --------------------------------------------------------- | ------- | --------- | ------------ | --------- | ------- | --------- |
| ticket-001 | Modernize pyproject.toml metadata and wheel configuration | epic-01 | completed | Detailed     | 0.97      | 1.00    | EXCELLENT |
| ticket-002 | Restructure CI workflow into parallel jobs                | epic-01 | completed | Detailed     | 0.97      | 1.00    | EXCELLENT |
| ticket-003 | Migrate docs deployment to official GitHub Pages actions  | epic-01 | completed | Detailed     | 0.97      | 0.95    | EXCELLENT |
| ticket-004 | Create release workflow with trusted publishing           | epic-01 | completed | Detailed     | 0.97      | 0.93    | EXCELLENT |
| ticket-005 | Add pre-commit hooks for ruff and mypy                    | epic-01 | completed | Detailed     | 0.97      | 0.93    | EXCELLENT |
| ticket-006 | Migrate Sphinx theme from sphinx-rtd-theme to Furo        | epic-02 | pending   | Detailed     | 0.97      | --      | --        |
| ticket-007 | Update sphinx-gallery examples for current API patterns   | epic-02 | pending   | Detailed     | 0.92      | --      | --        |
| ticket-008 | Create architecture documentation page                    | epic-03 | pending   | Outline      | --        | --      | --        |
| ticket-009 | Create FAQ documentation page                             | epic-03 | pending   | Outline      | --        | --      | --        |
| ticket-010 | Create performance guide documentation page               | epic-03 | pending   | Outline      | --        | --      | --        |
| ticket-011 | Improve API reference with autosummary                    | epic-03 | pending   | Outline      | --        | --      | --        |
| ticket-012 | Update index.rst toctree for new pages                    | epic-03 | pending   | Outline      | --        | --      | --        |
| ticket-013 | Expand README with badges and structured sections         | epic-04 | pending   | Outline      | --        | --      | --        |
| ticket-014 | Create CONTRIBUTING.md                                    | epic-04 | pending   | Outline      | --        | --      | --        |
| ticket-015 | Reformat CHANGELOG to Keep a Changelog standard           | epic-04 | pending   | Outline      | --        | --      | --        |
| ticket-016 | Update installation documentation for uv workflow         | epic-04 | pending   | Outline      | --        | --      | --        |
