# Accumulated Learnings — Through Epic 02

## From Epic 01

- `exec(open('__init__.py').read())` fails with relative imports; use regex extraction
- mypy `strict` re-enables `warn_return_any`; must repeat `warn_return_any = false` in overrides
- cfinterface 1.8.3 vs >=1.9.0 conflict blocks mypy and sphinx-gallery execution
- ruff formatted 93 files on first run; per-file-ignores needed for `examples/*.py` E402
- `uv run --no-sync` bypasses lockfile validation for pre-commit hooks

## From Epic 02

- Furo theme migration is straightforward: change `html_theme`, remove RTD from extensions, replace theme options
- `pygments_dark_style = "monokai"` needed for dark mode syntax highlighting
- sphinx-gallery example execution fails due to cfinterface import errors (same root cause as mypy)
- Only `examples/plot_forward.py` had deprecated `set_version` reference; all other examples already used current API
- All documentation content MUST remain in Brazilian Portuguese per master plan
- Code simplifiers must be carefully reviewed — they may translate Portuguese content to English
- Subdirectories under `examples/` contain only data files, no Python scripts to review
