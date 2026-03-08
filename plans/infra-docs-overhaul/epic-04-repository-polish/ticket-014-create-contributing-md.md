# ticket-014 Create CONTRIBUTING.md

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Create a comprehensive CONTRIBUTING.md file in Brazilian Portuguese that covers development environment setup (using uv), coding standards (ruff, mypy strict, naming conventions), testing procedures (pytest, pytest-xdist), pre-commit hook setup, pull request workflow, and the cfinterface framework modeling guidelines. This replaces the limited contribution guidance currently in `docs/source/geral/contribuicao.rst` with a standalone, discoverable file.

## Anticipated Scope

- **Files likely to be modified**: `/home/rogerio/git/inewave/CONTRIBUTING.md` (new), possibly `docs/source/geral/contribuicao.rst` (update to reference CONTRIBUTING.md or be replaced)
- **Key decisions needed**: Whether to keep the existing `contribuicao.rst` and link to CONTRIBUTING.md, or replace it entirely; how much of the cfinterface framework explanation to include vs. linking to cfinterface docs; whether to include a DCO or CLA requirement
- **Open questions**: Should the CONTRIBUTING.md reference the pre-commit configuration from ticket-005? Should it include a section on the versioning/release process? Should it mention the benchmark suite and how to add benchmarks?

## Dependencies

- **Blocked By**: ticket-005-add-pre-commit-hooks.md (contribution guide should reference pre-commit setup)
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
