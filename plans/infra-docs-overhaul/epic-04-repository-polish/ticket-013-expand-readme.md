# ticket-013 Expand README with Badges and Structured Sections

## Context

### Background

The current `README.md` is minimal: it has two badges (CI tests, codecov), a brief description, pip-based installation instructions, and a link to the documentation. After three epics of modernization — parallel CI jobs, Furo-themed Sphinx docs, new architecture/FAQ/performance pages, pre-commit hooks, and release workflow — the README no longer reflects the project's maturity. It must be expanded to serve as the primary landing page on GitHub and PyPI with comprehensive badges, feature highlights, a quick-start code example, and structured navigation to documentation.

### Relation to Epic

This is the first ticket in Epic 4 (Repository Polish). It establishes the project's public-facing presentation. The expanded README will reference documentation URLs, CI workflows, and tooling set up in earlier epics.

### Current State

The file `/home/rogerio/git/inewave/README.md` contains:

- A `tests` badge pointing to `workflows/tests/badge.svg` (stale — the workflow was renamed to `CI` in ticket-002)
- A codecov badge (functional)
- A 3-paragraph description in Portuguese
- pip-based installation commands (outdated — uv is the modern workflow)
- A link to the docs site

The CI workflow name is `CI` (defined in `.github/workflows/main.yml`). The docs site is at `https://rjmalves.github.io/inewave`. The license is MIT. Python versions supported are 3.10, 3.11, 3.12 (from `pyproject.toml` classifiers). The PyPI package name is `inewave`.

## Specification

### Requirements

1. Replace the stale `tests` badge with a CI badge pointing to the correct workflow name `CI`
2. Add badges for: PyPI version, Python versions, license (MIT), documentation link
3. Keep the existing codecov badge (it is functional)
4. Add a "Funcionalidades" (Features) section with bullet points highlighting key capabilities
5. Add a "Exemplo Rapido" (Quick Start) section with a minimal code example showing file reading and DataFrame access
6. Restructure installation section to show `pip install inewave` as the primary method (this is README for end users, not developers)
7. Add a "Documentacao" section with links to specific doc pages: tutorial, architecture, FAQ, performance guide, API reference
8. Add a "Contribuindo" section with a short paragraph pointing to `CONTRIBUTING.md`
9. Add a "Licenca" section referencing the MIT license
10. All text content in Brazilian Portuguese

### Inputs/Props

- Badge URLs derived from: GitHub Actions CI workflow name `CI`, codecov token, PyPI package `inewave`, license `MIT`
- Documentation URL: `https://rjmalves.github.io/inewave`
- Repository URL: `https://github.com/rjmalves/inewave`

### Outputs/Behavior

A fully restructured `README.md` that renders correctly on GitHub with all badges visible and linking to the correct targets.

### Error Handling

Not applicable — this is a static markdown file.

## Acceptance Criteria

- [ ] Given the file `/home/rogerio/git/inewave/README.md` is opened on GitHub, when the page renders, then the CI badge URL contains `workflows/CI/badge.svg` (not `workflows/tests/badge.svg`)
- [ ] Given the file `/home/rogerio/git/inewave/README.md`, when inspected, then it contains badges for: CI status, codecov, PyPI version, Python versions, license, and documentation
- [ ] Given the file `/home/rogerio/git/inewave/README.md`, when inspected, then it contains a "Funcionalidades" section with at least 4 bullet points describing key features
- [ ] Given the file `/home/rogerio/git/inewave/README.md`, when inspected, then it contains an "Exemplo Rapido" section with a Python code block showing `from inewave.newave import ...`, a `.read()` call, and a `.valores` DataFrame access
- [ ] Given the file `/home/rogerio/git/inewave/README.md`, when inspected, then all prose content is in Brazilian Portuguese (no English section headings or descriptions)

## Implementation Guide

### Suggested Approach

1. Open `/home/rogerio/git/inewave/README.md`
2. Replace the entire content with the new structured README
3. Badge block at top:
   - CI: `![CI](https://github.com/rjmalves/inewave/actions/workflows/main.yml/badge.svg)`
   - Codecov: keep existing `[![codecov](...)](...)`
   - PyPI: `[![PyPI version](https://img.shields.io/pypi/v/inewave)](https://pypi.org/project/inewave/)`
   - Python: `[![Python versions](https://img.shields.io/pypi/pyversions/inewave)](https://pypi.org/project/inewave/)`
   - License: `[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)`
   - Docs: `[![Documentacao](https://img.shields.io/badge/docs-online-blue)](https://rjmalves.github.io/inewave)`
4. Keep the existing introductory paragraph about NEWAVE/CEPEL (it is well-written)
5. Add sections in order: Funcionalidades, Exemplo Rapido, Instalacao, Documentacao, Contribuindo, Licenca
6. For the quick-start example, use a simple pattern like reading `pmo.dat` — this is the most commonly used file and appears in existing examples
7. Installation section: show `pip install inewave` as primary, `pip install git+...` as development alternative — this is for end users, not contributors

### Key Files to Modify

- `/home/rogerio/git/inewave/README.md` — complete rewrite

### Patterns to Follow

- All documentation content in Brazilian Portuguese (per master plan and learnings)
- Use accented characters in headings where grammatically correct (e.g., "Instalacao" not "Instalação" because markdown headings with accents can cause anchor issues — verify behavior and use accents if anchors work)
- Badge format: image link wrapped in clickable link to the source

### Pitfalls to Avoid

- Do NOT reference `workflows/tests/badge.svg` — the workflow was renamed to `CI` in ticket-002; the file is `main.yml` so the badge URL uses `actions/workflows/main.yml/badge.svg`
- Do NOT add a badge for pre-commit — pre-commit is a development tool, not user-facing
- Do NOT include detailed development setup instructions — that belongs in CONTRIBUTING.md (ticket-014)
- Do NOT translate the code example to English — variable names in code stay as-is from the library API
- Do NOT reference `sintetizador-newave` — it is a separate project and out of scope

## Testing Requirements

### Unit Tests

Not applicable — documentation file.

### Integration Tests

Not applicable.

### E2E Tests (if applicable)

Not applicable. Manual verification: open the rendered README on GitHub and confirm all badges load and all links resolve.

## Dependencies

- **Blocked By**: ticket-002-restructure-ci-workflow.md (CI badge URL depends on the workflow file name `main.yml`), ticket-005-add-pre-commit-hooks.md (pre-commit is set up, confirming dev tooling is ready)
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High
