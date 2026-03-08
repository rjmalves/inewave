# ticket-016 Update Installation Documentation for uv Workflow

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Update the Sphinx installation documentation page at `docs/source/geral/instalacao.rst` to reflect the modern uv-based development workflow, including uv installation, `uv sync` commands for different dependency groups, and development environment setup. The current page references `pip install` and `dev-requirements.txt` which are outdated.

## Anticipated Scope

- **Files likely to be modified**: `docs/source/geral/instalacao.rst`
- **Key decisions needed**: Whether to show both pip and uv installation methods or recommend uv exclusively; whether to include virtual environment setup instructions; how to handle the dependency groups (test, lint, docs) from ticket-001
- **Open questions**: Should the installation page cover development setup or keep that in CONTRIBUTING.md? Should it mention Python version requirements prominently? Should it include a section on verifying the installation?

## Dependencies

- **Blocked By**: ticket-001-modernize-pyproject-toml.md (dependency groups must be finalized), ticket-006-migrate-sphinx-theme.md (page should render with Furo)
- **Blocks**: None

## Effort Estimate

**Points**: 1
**Confidence**: Low (will be re-estimated during refinement)
