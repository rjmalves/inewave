# Epic 4: Repository Polish

## Goals

Bring repository-level files (README, CONTRIBUTING, CHANGELOG, installation docs) to a professional standard with comprehensive content, consistent formatting, and actionable guidance for users and contributors.

## Scope

- Expand README with full badge set, feature highlights, quick-start example, and section structure
- Create CONTRIBUTING.md with development setup, coding standards, PR workflow, and testing procedures
- Reformat CHANGELOG to follow the Keep a Changelog standard
- Update installation documentation in Sphinx to reflect current uv-based workflow

## Out of Scope

- Modifying library source code or tests
- Creating new Sphinx documentation pages (done in Epic 3)
- Changing the CI/CD pipeline (done in Epic 1)
- Adding a CODE_OF_CONDUCT.md or SECURITY.md

## Tickets

| Ticket     | Title                                             | Effort |
| ---------- | ------------------------------------------------- | ------ |
| ticket-013 | Expand README with badges and structured sections | 2      |
| ticket-014 | Create CONTRIBUTING.md                            | 3      |
| ticket-015 | Reformat CHANGELOG to Keep a Changelog standard   | 2      |
| ticket-016 | Update installation documentation for uv workflow | 1      |

## Dependencies

- **Blocked By**: None strictly, but best executed after Epic 1 (CI badges need to be correct) and Epic 2 (docs URL needs to be correct)
- ticket-014 (CONTRIBUTING) should reference the pre-commit setup from Epic 1

## Acceptance Criteria

- README renders correctly on GitHub with all badges showing valid status
- CONTRIBUTING.md covers development setup, coding standards, testing, and PR workflow
- CHANGELOG follows Keep a Changelog format with proper version headers, dates, and category grouping
- Installation docs reference `uv` as the recommended tooling
