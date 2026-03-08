# Accumulated Learnings — Epic 01: Packaging & CI Modernization

## Key Patterns (reuse in future epics)

- Each CI job installs only the extras it needs: `uv sync --extra lint | test | docs` — never `--dev` or `--all-extras` in CI; see `.github/workflows/main.yml`
- `dev` optional-dependency group is a self-referencing alias (`"inewave[test,lint,docs]"`) for local use only; see `pyproject.toml`
- Releases trigger on `push: tags: ["v*"]`, not `release: types: [created]`; version is validated by regex before build; see `.github/workflows/release.yml`
- GitHub Pages deployment uses `upload-pages-artifact@v3` + `deploy-pages@v4` with `concurrency: group: "pages"`; `peaceiris` is gone; see `.github/workflows/docs.yml`
- mypy pre-commit hook is `local`, `language: system`, `pass_filenames: false`, `stages: [manual]`; see `.pre-commit-config.yaml`

## Critical Pitfalls Discovered

- **`exec(open('__init__.py').read())` fails on relative imports** — `inewave/__init__.py` uses `from . import newave`; use `re.search(r'__version__ = "(.+?)"', ...)` instead; implemented in `.github/workflows/release.yml`
- **mypy `strict` re-enables `warn_return_any`** — setting it `false` in `[tool.mypy]` is not enough; must repeat `warn_return_any = false` inside every `[[tool.mypy.overrides]]` block that sets `strict = true`; see `pyproject.toml`
- **cfinterface 1.8.3 vs 1.9.0 conflict is unresolved** — `cfinterface>=1.9.0` is the pinned runtime dep but `<=1.8.3` is what works with the existing parsing model; this forces mypy pre-commit to `stages: [manual]` and may affect Sphinx autodoc in Epic 2
- **ruff first-run formatted 93 files** — formatting was never previously enforced; the churn in `inewave/newave/modelos/` is permanent and expected; these files are now stable

## Dependency Group Structure

- `test`: pytest, pytest-cov, pytest-xdist
- `lint`: mypy, pre-commit, ruff (alphabetical order enforced)
- `docs`: matplotlib, numpydoc, plotly, sphinx, sphinx-gallery, sphinx-rtd-theme
- `dev`: `inewave[test,lint,docs]`

## Ruff Configuration Notes

- `line-length = 80` in `[tool.ruff]`
- `per-file-ignores = { "examples/*.py" = ["E402"] }` — Sphinx Gallery scripts require top-level imports after code; add similar rules for any new script directories before running ruff
- Pre-commit hook pinned to `astral-sh/ruff-pre-commit@v0.15.5`

## Permissions Required for Workflows

- Docs deployment: `pages: write`, `id-token: write`
- Release: `contents: write` (for `gh release create`) + `id-token: write` (for PyPI OIDC trusted publishing)

## Warnings for Epic 2 (Sphinx Modernization)

- `uv sync --extra docs` resolves `cfinterface` as a transitive dep — verify the resolved version does not break Sphinx autodoc imports
- The `docs` job in `main.yml` currently uses `sphinx-rtd-theme`; Epic 2 will switch this to Furo — update both `pyproject.toml` `docs` group and `.github/workflows/docs.yml`
