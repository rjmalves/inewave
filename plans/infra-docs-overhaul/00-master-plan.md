# Master Plan: Infrastructure, CI/CD & Documentation Overhaul

## Executive Summary

Modernize the inewave project's packaging metadata, CI/CD pipelines, documentation infrastructure, and repository files to align with current Python ecosystem best practices. This overhaul brings the project's infrastructure and documentation quality to the same standard already achieved for code quality (mypy strict, ruff, benchmarks) in the v1.13.0 release.

## Goals & Non-Goals

### Goals

- Modernize `pyproject.toml` with complete classifiers, `py.typed` inclusion in wheel, and cleaned-up dev dependencies
- Restructure CI into parallel jobs (lint, typecheck, test, docs) for faster feedback
- Migrate docs deployment from deprecated `peaceiris/actions-gh-pages@v3` to official GitHub Pages actions
- Create a dedicated release workflow with trusted publishing (OIDC) and version-tag validation
- Add pre-commit hooks for ruff and mypy to catch issues before push
- Migrate Sphinx theme from `sphinx-rtd-theme` to Furo for modern appearance and better mobile support
- Update sphinx-gallery examples to use current best practices
- Expand documentation with architecture, FAQ, performance guide, and improved API reference pages
- Polish repository with expanded README, CONTRIBUTING.md, and reformatted CHANGELOG

### Non-Goals

- Migrating from pandas to Polars (inewave uses pandas; this is not changing)
- Adding mypy strict mode (already enabled across all submodules)
- Adding benchmarks (already exist in `benchmarks/`)
- Modifying the MIGRATION.md (already comprehensive for v1.13.0)
- Changing the lazy import mechanism or any library code
- Upgrading Python version requirements

## Architecture Overview

### Current State

- **Packaging**: `pyproject.toml` with Hatchling, but missing Python 3.11/3.12 classifiers, `py.typed` not included in wheel, local source override for `cfinterface`
- **CI**: Single sequential job (`main.yml`) running tests + mypy + ruff + sphinx-build in sequence across 3 Python versions; separate `docs.yml` using deprecated `peaceiris/actions-gh-pages@v3`; `publish.yml` with trusted publishing but triggered only by release events
- **Docs**: Sphinx with `sphinx-rtd-theme`, sphinx-gallery examples, numpydoc. Content is minimal: presentation, installation, tutorial, contribution guide, and API reference. All in Brazilian Portuguese
- **Repository**: Basic README with two badges, no CONTRIBUTING.md, CHANGELOG in simple heading format

### Target State

- **Packaging**: Complete classifiers (Python 3.10-3.12, typed), `py.typed` included in wheel, dev deps split into logical groups, local source override removed from committed config
- **CI**: Parallel jobs for lint, typecheck, test (matrix), docs build; official `actions/deploy-pages` for docs; dedicated release workflow with version validation
- **Docs**: Furo theme with dark mode, updated examples, architecture page, FAQ, performance guide, improved API reference with autosummary
- **Repository**: README with full badge set and sections, CONTRIBUTING.md, CHANGELOG in Keep a Changelog format

### Key Design Decisions

1. **Furo over RTD theme**: Furo provides better mobile support, dark mode, cleaner design, and is actively maintained. It is the de facto standard for modern Python projects
2. **Parallel CI jobs**: Each check (lint, type, test, docs) runs as an independent job, failing fast and reducing total wall-clock time
3. **Official GitHub Pages deployment**: `actions/deploy-pages@v4` + `actions/upload-pages-artifact@v3` replace the deprecated third-party action
4. **Pre-commit with ruff + mypy**: Catches formatting and type issues before code reaches CI
5. **Keep documentation language in Portuguese**: All new documentation content will be written in Brazilian Portuguese to match existing content

## Technical Approach

### Tech Stack

- Python 3.10+ with Hatchling build system
- GitHub Actions for CI/CD
- Sphinx + Furo for documentation
- ruff for linting, mypy for type checking
- pre-commit for local hooks

### Component/Module Breakdown

| Component               | Scope                                                             |
| ----------------------- | ----------------------------------------------------------------- |
| pyproject.toml          | Metadata, classifiers, dev deps, wheel config                     |
| .github/workflows/      | main.yml (parallel), docs.yml (official pages), release.yml (new) |
| .pre-commit-config.yaml | ruff + mypy hooks                                                 |
| docs/source/conf.py     | Furo theme, updated config                                        |
| docs/source/            | New content pages (architecture, FAQ, performance, API)           |
| README.md               | Expanded with badges, sections                                    |
| CONTRIBUTING.md         | New file                                                          |
| CHANGELOG.md            | Reformatted to Keep a Changelog                                   |

### Testing Strategy

- CI workflow changes validated by pushing to a feature branch and verifying all jobs pass
- Documentation changes validated by local `sphinx-build` and visual inspection
- Pre-commit hooks validated by running `pre-commit run --all-files` locally

## Phases & Milestones

| Phase | Epic                            | Milestone                                                                                             |
| ----- | ------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 1     | Packaging & CI Modernization    | All CI jobs green with parallel execution, docs deploying via official action, release workflow ready |
| 2     | Sphinx Modernization            | Docs building with Furo theme, examples updated                                                       |
| 3     | Documentation Content Expansion | Architecture, FAQ, performance guide, API reference pages live                                        |
| 4     | Repository Polish               | README expanded, CONTRIBUTING.md added, CHANGELOG reformatted                                         |

## Risk Analysis

| Risk                                                             | Probability | Impact | Mitigation                                                        |
| ---------------------------------------------------------------- | ----------- | ------ | ----------------------------------------------------------------- |
| Furo theme breaks existing custom CSS or RST directives          | Medium      | Low    | Review all RST files for RTD-specific directives before migration |
| sphinx-gallery examples fail with current plotting libraries     | Low         | Medium | Test each example locally before committing                       |
| Pre-commit mypy hook too slow for developer workflow             | Medium      | Low    | Configure mypy hook to run only on changed files                  |
| `peaceiris/actions-gh-pages` removal breaks deploy mid-migration | Low         | High   | Migrate docs workflow in a single atomic commit                   |

## Success Metrics

- CI pipeline wall-clock time reduced by 40%+ through parallelization
- All CI checks pass on the feature branch before merge
- Documentation site renders correctly with Furo theme on desktop and mobile
- `pre-commit run --all-files` passes cleanly
- README renders with all badges showing correct status
- CHANGELOG follows Keep a Changelog format with proper date and link annotations
