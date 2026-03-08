# Accumulated Learnings — Through Epic 03

## From Epic 01

- `exec(open('__init__.py').read())` fails with relative imports; use regex extraction
- mypy `strict` re-enables `warn_return_any`; must repeat `warn_return_any = false` in overrides
- cfinterface 1.8.3 vs >=1.9.0 conflict blocks mypy and sphinx-gallery execution
- ruff formatted 93 files on first run; per-file-ignores needed for `examples/*.py` E402
- `uv run --no-sync` bypasses lockfile validation for pre-commit hooks

## From Epic 02

- Furo theme migration is straightforward: change `html_theme`, remove RTD from extensions, replace theme options
- `pygments_dark_style = "monokai"` needed for dark mode syntax highlighting
- sphinx-gallery example execution fails due to cfinterface import errors
- All documentation content MUST remain in Brazilian Portuguese per master plan
- Code simplifiers must be carefully reviewed — they may translate Portuguese content to English

## From Epic 03

- RST documentation pages are best organized under `docs/source/geral/` for content pages
- `.. autosummary:: :nosignatures:` without `:toctree:` adds summary tables without duplicating per-file RST pages
- The `_LAZY_IMPORTS` dict in each module's `__init__.py` is the canonical source for public class lists
- `_templates/layout.html` had stale RTD-specific CSS that was cleaned to `{% extends "!layout.html" %}`
- New toctree section "Guias" inserted between "Geral" and "Referência" for architecture/performance/FAQ pages
- Sphinx build `toc.not_included` warnings are expected for pages not yet in toctree — resolved by ticket-012
- Performance numbers should always use `~` prefix and include hardware/Python caveat note
- FAQ structure: 5 sections with 15+ questions, `**bold question?**` format, `.. code-block::` for answers
