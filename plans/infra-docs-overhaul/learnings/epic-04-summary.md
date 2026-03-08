# Accumulated Learnings — Through Epic 04 (Final)

## Python / Tooling

- `exec(open('__init__.py').read())` fails with relative imports; use regex extraction instead
- mypy `strict` re-enables `warn_return_any`; must repeat `warn_return_any = false` in per-module overrides
- cfinterface 1.8.3 vs >=1.9.0 conflict blocks mypy and sphinx-gallery; pin `cfinterface<=1.8.3` as workaround
- ruff formatted 93 files on first run; per-file-ignores needed for `examples/*.py` (E402)
- `uv run --no-sync` bypasses lockfile validation for pre-commit hook entry points
- All tool invocations in documentation and CI use `uv run` prefix: `uv run ruff check`, `uv run mypy`, `uv run pytest`

## Sphinx / Documentation

- Furo theme migration: change `html_theme`, remove RTD from extensions, replace theme options
- `pygments_dark_style = "monokai"` required for dark mode syntax highlighting in Furo
- sphinx-gallery example execution fails when cfinterface import errors occur at collection time
- All documentation content MUST remain in Brazilian Portuguese; code simplifiers risk translating it to English
- RST content pages go under `docs/source/geral/`; file names must match toctree references exactly
- `.. autosummary:: :nosignatures:` without `:toctree:` adds summary tables without creating per-file RST pages
- `_templates/layout.html` with stale RTD-specific CSS must be replaced with `{% extends "!layout.html" %}`
- `.. code-block:: bash` (or `:: python`) required for all shell/code examples in Furo — `::` literal blocks get no syntax highlighting
- Sphinx `toc.not_included` warnings are expected for pages not yet referenced in any toctree

## Documentation Content Conventions

- New toctree section "Guias" sits between "Geral" and "Referencia" for architecture/performance/FAQ pages
- Performance numbers prefixed with `~` (approximate); include hardware/Python version caveat in a note block
- FAQ structure: 5 sections, 15+ questions, `**bold question?**` format, `.. code-block::` for code answers
- `_LAZY_IMPORTS` dict in each module's `__init__.py` is the canonical list of public classes for autosummary tables
- When a root `CONTRIBUTING.md` is added, `contribuicao.rst` becomes a thin wrapper: `.. note::` redirect at top + retain only Sphinx-specific cross-references (`:obj:~cfinterface...`, `:ref:`)
- End-user installation docs (`instalacao.rst`) show pip first, uv second; development setup redirects to `CONTRIBUTING.md`

## Repository-Level Files

- README badge order: CI (Actions URL), codecov, PyPI version, PyPI Python versions, License (shields.io), Docs (shields.io)
- CI badge URL: `actions/workflows/main.yml/badge.svg` — NOT `workflows/<workflow-name>/badge.svg`
- Markdown heading anchors: avoid accented characters (use "Instalacao" not "Instalação") to prevent GitHub anchor issues
- README "Exemplo Rapido" uses two blocks: one read-only (`.read()` + property access) + one read-modify-write (`.write()`)
- Developer commands (uv, pre-commit, pytest) belong in `CONTRIBUTING.md`, not in end-user README
- Shell commands in documentation use `$` prefix consistently; `uv run` prefix on all tool invocations

## CHANGELOG Conventions

- KAC heading format: `## [X.Y.Z] - YYYY-MM-DD`; brackets without `v` prefix; comparison links use `v` prefix in tag names
- Portuguese KAC category names: `### Adicionado`, `### Modificado`, `### Corrigido`, `### Descontinuado`, `### Removido`
- Unreleased version: `## [X.Y.Z] - Unreleased` (preserves version number in heading; do NOT use plain `## [Unreleased]`)
- Comparison links section required at bottom; first version uses `releases/tag/vX.Y.Z`, all others use `compare/vA...vB`
- Pre-compute git tag date mapping at planning time with `git tag --format='%(refname:short) %(creatordate:short)'`; embed in ticket to avoid git access at implementation time

## Planning Insights

- Documentation-only epics (no source code changes) consistently score quality 1.0 on lint/type-safety/test-delta dimensions (non-code file detection applies)
- Tickets for static file rewrites benefit from embedding the full target structure in the spec (date maps, badge URLs, section outlines) — reduces ambiguity and implementation round-trips
- When splitting contributor docs between root Markdown and in-Sphinx RST, specify in the ticket which content belongs where: root file for GitHub-discoverable setup/workflow, RST for Sphinx-only rendering features
