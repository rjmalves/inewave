# ticket-016 Update Installation Documentation for uv Workflow

## Context

### Background

The Sphinx installation page at `docs/source/geral/instalacao.rst` is outdated. It references Python >= 3.8 (now >= 3.10), `pip` as the sole package manager, and `python -m pip install --upgrade pip` as a prerequisite step. After Epic 1 modernized the project to use uv and restructured dependency groups in `pyproject.toml`, the installation docs must reflect the current tooling.

### Relation to Epic

Fourth and final ticket in Epic 4 (Repository Polish). It updates the last piece of outdated documentation — the Sphinx installation page. This ticket focuses on the end-user installation page in Sphinx; developer setup is covered in CONTRIBUTING.md (ticket-014).

### Current State

The file `/home/rogerio/git/inewave/docs/source/geral/instalacao.rst`:

- States Python >= 3.8 compatibility (incorrect — `pyproject.toml` specifies `>= 3.10`)
- Recommends upgrading pip with `python -m pip install --upgrade pip`
- Shows `pip install inewave` for stable, `pip install git+...` for development
- References venv documentation
- Does not mention uv at all
- Uses `::` (literal block) syntax for code examples (no language highlighting)

The page renders in Sphinx under the "Geral" toctree section. It uses Furo theme (migrated in ticket-006).

## Specification

### Requirements

1. Update Python version requirement from `>= 3.8` to `>= 3.10`
2. Keep `pip install inewave` as the primary installation method for end users (pip is universal; uv is for development)
3. Add a new section for uv-based installation as an alternative: `uv add inewave` or `uv pip install inewave`
4. Remove the `python -m pip install --upgrade pip` prerequisite paragraph (unnecessary noise)
5. Update the development installation section to use `uv sync --extra dev` instead of `pip install -r dev-requirements.txt`
6. Use `.. code-block:: bash` for code examples instead of `::` literal blocks (enables syntax highlighting with Furo)
7. Add a brief note about Python version requirements prominently near the top
8. Keep all text in Brazilian Portuguese

### Inputs/Props

- Current file: `/home/rogerio/git/inewave/docs/source/geral/instalacao.rst`
- Python requirement: `>= 3.10` (from `pyproject.toml`)
- Supported Python versions: 3.10, 3.11, 3.12 (from classifiers)
- Package name: `inewave`
- Repository URL: `https://github.com/rjmalves/inewave`

### Outputs/Behavior

An updated `instalacao.rst` that renders correctly in Sphinx with Furo theme, showing current installation methods with syntax-highlighted code blocks.

### Error Handling

Not applicable — static RST documentation file.

## Acceptance Criteria

- [ ] Given the file `/home/rogerio/git/inewave/docs/source/geral/instalacao.rst`, when inspected, then it states Python `>= 3.10` (not `>= 3.8`)
- [ ] Given the file `/home/rogerio/git/inewave/docs/source/geral/instalacao.rst`, when inspected, then it contains `pip install inewave` as the primary installation command
- [ ] Given the file `/home/rogerio/git/inewave/docs/source/geral/instalacao.rst`, when inspected, then it contains a section mentioning `uv` as an alternative installation method
- [ ] Given the file `/home/rogerio/git/inewave/docs/source/geral/instalacao.rst`, when inspected, then it does not contain `python -m pip install --upgrade pip` or reference `dev-requirements.txt`
- [ ] Given the file `/home/rogerio/git/inewave/docs/source/geral/instalacao.rst`, when inspected, then all code examples use `.. code-block:: bash` directive (not `::` literal blocks)

## Implementation Guide

### Suggested Approach

1. Read `/home/rogerio/git/inewave/docs/source/geral/instalacao.rst`
2. Rewrite the file with the following structure:

   ```
   Instalacao
   ==========

   O *inewave* e compativel com versoes de Python >= 3.10 (testado em 3.10, 3.11 e 3.12).

   Instalando com pip
   ------------------
   (pip install inewave, pip install --upgrade inewave, pip install inewave==x.y.z)

   Instalando com uv
   -----------------
   (uv add inewave, or uv pip install inewave)

   Instalando a versao de desenvolvimento
   ---------------------------------------
   (git clone, uv sync --extra dev — point to CONTRIBUTING.md for full setup)

   Verificando a instalacao
   ------------------------
   (python -c "import inewave; print(inewave.__version__)")
   ```

3. Use `.. code-block:: bash` for all shell command blocks
4. Use `.. code-block:: python` for the verification example
5. Keep the venv recommendation paragraph but simplify it
6. Remove the `pip --upgrade pip` prerequisite entirely

### Key Files to Modify

- `/home/rogerio/git/inewave/docs/source/geral/instalacao.rst` — rewrite

### Patterns to Follow

- RST documentation pages organized under `docs/source/geral/` (learnings from Epic 3)
- Use `.. code-block:: bash` for shell examples (consistent with architecture and performance pages from Epic 3)
- All content in Brazilian Portuguese
- Reference `CONTRIBUTING.md` for full development setup (per ticket-014)

### Pitfalls to Avoid

- Do NOT recommend uv as the only installation method — many end users use pip and do not have uv installed
- Do NOT include full development environment setup — that belongs in CONTRIBUTING.md
- Do NOT change the file name or path — it is referenced in `docs/source/index.rst` toctree as `geral/instalacao`
- Do NOT use `::` for code blocks — use explicit `.. code-block::` directives for proper syntax highlighting with Furo theme

## Testing Requirements

### Unit Tests

Not applicable — documentation file.

### Integration Tests

Not applicable.

### E2E Tests (if applicable)

Not applicable. Manual verification: run `uv run sphinx-build -M html docs/source docs/build` and confirm the page renders without warnings and code blocks are syntax-highlighted.

## Dependencies

- **Blocked By**: ticket-001-modernize-pyproject-toml.md (dependency groups finalized), ticket-006-migrate-sphinx-theme.md (Furo theme active)
- **Blocks**: None

## Effort Estimate

**Points**: 1
**Confidence**: High
