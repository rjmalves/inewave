# ticket-014 Create CONTRIBUTING.md

## Context

### Background

The project currently has contribution guidance only in `docs/source/geral/contribuicao.rst`, which is outdated: it references `pip install -r dev-requirements.txt`, `pylama` (replaced by ruff in v1.9.0), and `black` (replaced by ruff-format). It does not cover pre-commit hooks, uv-based setup, mypy strict mode, or the modern PR workflow. A standalone `CONTRIBUTING.md` at the repository root is the standard discoverable location for GitHub (auto-linked in the "Contributing" sidebar).

After Epic 1, the project uses uv for package management, ruff + ruff-format via pre-commit hooks (with mypy as a manual-stage hook), parallel CI jobs (lint, typecheck, test, docs), and a tag-triggered release workflow. This ticket creates a comprehensive `CONTRIBUTING.md` reflecting all of this.

### Relation to Epic

Second ticket in Epic 4 (Repository Polish). It provides the contributor-facing counterpart to ticket-013's user-facing README. The README's "Contribuindo" section will point here.

### Current State

- No `CONTRIBUTING.md` exists at the repository root
- `docs/source/geral/contribuicao.rst` exists with outdated content: references `pip`, `dev-requirements.txt`, `pylama`, `black`
- Pre-commit config at `.pre-commit-config.yaml`: ruff (lint + format) on commit, mypy as manual stage
- CI workflow at `.github/workflows/main.yml`: parallel jobs for lint, typecheck, test (matrix 3.10-3.12), docs
- Release workflow at `.github/workflows/release.yml`: tag-triggered PyPI publishing
- Dependency groups in `pyproject.toml`: `test`, `lint`, `docs`, `dev` (meta-group combining all three)
- pytest with pytest-xdist for parallel test execution, pytest-cov for coverage
- mypy strict mode for all inewave submodules

## Specification

### Requirements

1. Create `/home/rogerio/git/inewave/CONTRIBUTING.md` in Brazilian Portuguese
2. Include sections:
   - **Configuracao do Ambiente de Desenvolvimento**: clone, `uv sync --extra dev`, pre-commit install
   - **Ferramentas de Qualidade de Codigo**: ruff (linting + formatting), mypy strict, pre-commit hooks
   - **Executando Testes**: `uv run pytest ./tests`, parallel execution with `-n auto`, coverage with `--cov`
   - **Framework cfinterface**: brief explanation of BlockFile/SectionFile/RegisterFile taxonomy and naming conventions (condensed from existing `contribuicao.rst`)
   - **Convencoes de Codigo**: PascalCase classes, snake_case properties/columns, Brazilian Portuguese for docstrings and documentation
   - **Fluxo de Pull Request**: fork, branch, commit, push, open PR, CI checks must pass
3. Update `docs/source/geral/contribuicao.rst` to become a thin wrapper that includes a brief intro and directs readers to the repository `CONTRIBUTING.md` for the full guide, while preserving the cfinterface framework explanation (which is documentation-specific and renders well in Sphinx with cross-references)

### Inputs/Props

- Pre-commit config: `.pre-commit-config.yaml` (ruff hooks + mypy manual)
- Dependency groups: `test`, `lint`, `docs`, `dev` from `pyproject.toml`
- Test command: `uv run pytest ./tests` (parallel: `uv run pytest -n auto ./tests`)
- Lint command: `uv run ruff check ./inewave`
- Format command: `uv run ruff format ./inewave`
- Typecheck command: `uv run mypy ./inewave`

### Outputs/Behavior

- A new file `/home/rogerio/git/inewave/CONTRIBUTING.md` rendered correctly on GitHub
- An updated `/home/rogerio/git/inewave/docs/source/geral/contribuicao.rst` that is shorter but still renders in Sphinx with cfinterface cross-references

### Error Handling

Not applicable — static documentation files.

## Acceptance Criteria

- [ ] Given the file `/home/rogerio/git/inewave/CONTRIBUTING.md` exists, when inspected, then it contains a section with `uv sync --extra dev` as the dependency installation command (not `pip install -r dev-requirements.txt`)
- [ ] Given the file `/home/rogerio/git/inewave/CONTRIBUTING.md`, when inspected, then it contains a section listing `uv run ruff check ./inewave`, `uv run ruff format ./inewave`, and `uv run mypy ./inewave` as the quality check commands
- [ ] Given the file `/home/rogerio/git/inewave/CONTRIBUTING.md`, when inspected, then it contains `pre-commit install` in the development setup instructions
- [ ] Given the file `/home/rogerio/git/inewave/CONTRIBUTING.md`, when inspected, then it contains a section about running tests with `uv run pytest ./tests` and mentions `-n auto` for parallel execution
- [ ] Given the file `/home/rogerio/git/inewave/docs/source/geral/contribuicao.rst`, when inspected, then it no longer references `pip install -r dev-requirements.txt`, `pylama`, or `black`

## Implementation Guide

### Suggested Approach

1. Create `/home/rogerio/git/inewave/CONTRIBUTING.md` with the following structure:

   ```
   # Contribuindo para o inewave

   ## Configuracao do Ambiente de Desenvolvimento
   (clone, uv install, uv sync --extra dev, pre-commit install)

   ## Ferramentas de Qualidade de Codigo
   (ruff check, ruff format, mypy --strict, pre-commit hooks explanation)

   ## Executando Testes
   (pytest, pytest-xdist -n auto, pytest-cov)

   ## Convencoes de Codigo
   (PascalCase, snake_case, typing, Portuguese docs)

   ## Modelagem de Arquivos com cfinterface
   (condensed BlockFile/SectionFile/RegisterFile explanation)

   ## Fluxo de Pull Request
   (fork, branch, implement, test, PR, CI)
   ```

2. Update `/home/rogerio/git/inewave/docs/source/geral/contribuicao.rst`:
   - Keep the title "Como contribuir?"
   - Keep the cfinterface framework section (it has Sphinx cross-references like `:obj:` that only work in RST)
   - Replace the outdated "dependencias de desenvolvimento" section with instructions using `uv`
   - Replace the "Procedimentos de teste" section with updated commands
   - Add a note at the top directing to `CONTRIBUTING.md` on GitHub for the full contributor guide

### Key Files to Modify

- `/home/rogerio/git/inewave/CONTRIBUTING.md` — new file
- `/home/rogerio/git/inewave/docs/source/geral/contribuicao.rst` — update outdated sections

### Patterns to Follow

- All prose in Brazilian Portuguese (learnings: "All documentation content MUST remain in Brazilian Portuguese")
- Use code blocks with shell commands prefixed with `$` for consistency with existing `contribuicao.rst`
- Use `uv run` prefix for all tool invocations (consistent with CI workflow in `main.yml`)
- Use `uv run --no-sync` for pre-commit hook entry (consistent with `.pre-commit-config.yaml`)

### Pitfalls to Avoid

- Do NOT delete `contribuicao.rst` entirely — it is referenced in the `index.rst` toctree under "Geral" and contains Sphinx-specific cross-references (`:obj:~cfinterface.files...`) that cannot be expressed in plain markdown
- Do NOT include a DCO or CLA requirement — none exists and adding one is out of scope
- Do NOT include versioning/release process details — that is maintainer-only information, not contributor guidance
- Do NOT reference benchmarks — the benchmark suite is internal tooling

## Testing Requirements

### Unit Tests

Not applicable — documentation files.

### Integration Tests

Not applicable.

### E2E Tests (if applicable)

Not applicable. Manual verification: confirm `CONTRIBUTING.md` renders on GitHub and `contribuicao.rst` builds with `uv run sphinx-build -M html docs/source docs/build` without warnings.

## Dependencies

- **Blocked By**: ticket-005-add-pre-commit-hooks.md (CONTRIBUTING references pre-commit setup)
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High
