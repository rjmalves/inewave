# Epic 01 Learnings — Packaging & CI Modernization

## Patterns Established

- **Dependency-group-scoped CI jobs**: Each GitHub Actions job installs only the extras it needs (`uv sync --extra lint`, `--extra test`, `--extra docs`) rather than the full dev set. Observe this pattern in `/home/rogerio/git/inewave/.github/workflows/main.yml`.
- **Self-referencing dev extra**: The `dev` group is defined as `"inewave[test,lint,docs]"` in `pyproject.toml`, so a single `uv sync --all-extras --dev` still installs everything for local development. See `/home/rogerio/git/inewave/pyproject.toml` `[project.optional-dependencies]`.
- **Tag-triggered release workflow**: The release pipeline triggers on `push: tags: ["v*"]` rather than `release: types: [created]`, validating version consistency before building. See `/home/rogerio/git/inewave/.github/workflows/release.yml`.
- **Official GitHub Pages artifact pattern**: Deployment uses `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4` with a `concurrency` group named `"pages"` to prevent race conditions. See `/home/rogerio/git/inewave/.github/workflows/docs.yml`.
- **local-repo mypy pre-commit hook**: mypy runs as a `local` hook with `language: system` and `pass_filenames: false` so it uses the project virtualenv and analyzes the whole package at once. See `/home/rogerio/git/inewave/.pre-commit-config.yaml`.

## Architectural Decisions

- **mypy demoted to manual stage in pre-commit**: mypy was configured with `stages: [manual]` instead of the default commit stage. Rationale: `cfinterface 1.8.3` (the pinned version that works with NEWAVE's data model) is missing type stubs, causing mypy to fail in pre-commit's isolated environment even with `language: system`. Running `pre-commit run mypy --hook-stage manual` still works for developers who explicitly invoke it, while the CI `typecheck` job remains the authoritative gate. Alternative of bumping to `cfinterface>=1.9.0` was rejected because it introduces breaking changes in the core parsing engine. File: `/home/rogerio/git/inewave/.pre-commit-config.yaml`.
- **Regex-based version extraction in release workflow**: The `Validate version matches tag` step uses `re.search(r'__version__ = "(.+?)"', ...)` instead of the ticket's suggested `exec(open('inewave/__init__.py').read())`. Rationale: `__init__.py` uses relative imports (`from . import newave`), which fail when executed outside a package context via `exec()`. Regex extraction is robust regardless of import structure. File: `/home/rogerio/git/inewave/.github/workflows/release.yml` line 26.
- **`warn_return_any = false` at both global and override scope**: mypy's `strict` mode re-enables `warn_return_any`; having it only at the `[tool.mypy]` global level is not enough when `[[tool.mypy.overrides]]` sets `strict = true` for all submodules. The override block must also set `warn_return_any = false`. File: `/home/rogerio/git/inewave/pyproject.toml` lines 66-75.
- **`uv run --no-sync` in pre-commit entry**: The mypy hook uses `entry: uv run --no-sync mypy ./inewave` to avoid uv attempting a sync (which would fail without network access or lock file write permission inside the hook runner). File: `/home/rogerio/git/inewave/.pre-commit-config.yaml`.

## Files & Structures Created

- `/home/rogerio/git/inewave/pyproject.toml` — Modernized with split optional-dependency groups (`test`, `lint`, `docs`, `dev`), Python 3.11/3.12 classifiers, `Typing :: Typed` classifier, Portuguese description, `uv.sources` removed.
- `/home/rogerio/git/inewave/.github/workflows/main.yml` — Replaced single sequential job with four parallel jobs: `lint`, `typecheck`, `test` (matrix), `docs`.
- `/home/rogerio/git/inewave/.github/workflows/docs.yml` — Migrated from `peaceiris/actions-gh-pages@v3` to official `upload-pages-artifact` + `deploy-pages` pattern with `concurrency` guard.
- `/home/rogerio/git/inewave/.github/workflows/release.yml` — New file (replaced `publish.yml`); tag-triggered, version-validating, trusted-publishing release pipeline.
- `/home/rogerio/git/inewave/.pre-commit-config.yaml` — New file; ruff hooks from `astral-sh/ruff-pre-commit@v0.15.5`, mypy as manual-stage local hook.

## Conventions Adopted

- **Ruff version pinning**: Pre-commit hooks pin the full ruff version (e.g., `v0.15.5`) at `/home/rogerio/git/inewave/.pre-commit-config.yaml`. Future hook updates should match the version used in CI to keep results consistent.
- **Alphabetical dependency ordering**: Dependencies within each optional-dependency group in `pyproject.toml` are sorted alphabetically. New additions must maintain this order.
- **`uv sync --extra <group>` per job**: All CI jobs use this pattern — never `uv sync --dev` or `uv sync --all-extras` in CI, to keep job installs fast and scoped.
- **`per-file-ignores` for examples/**: Sphinx Gallery example scripts use top-level imports after module-level code, triggering ruff E402. The `pyproject.toml` `[tool.ruff.lint]` section carries `per-file-ignores = { "examples/*.py" = ["E402"] }` to suppress this across the whole examples directory.
- **`contents: write` + `id-token: write` for release jobs**: Both permissions are required together — `id-token: write` for PyPI trusted publishing (OIDC) and `contents: write` for `gh release create`. Missing either causes a 403 in CI.

## Surprises & Deviations

- **ruff auto-formatted 93 files on first run**: The project had never enforced ruff formatting. Running `ruff format` for the first time produced 93 changed files (mainly `inewave/newave/modelos/`). This was expected to be a small config-only change; instead it touched a large portion of the source tree. The formatting pass is included in the uncommitted diff. Future epics should not be surprised by churn in these files — the formatting is now stable and consistent.
- **`exec(open(...).read())` approach fails for this `__init__.py`**: The ticket's implementation guide suggested using `exec()` to extract `__version__`. This fails because `inewave/__init__.py` contains `from . import newave` (relative import), which raises `ImportError` when run in a non-package context. The implemented solution uses regex instead. File: `/home/rogerio/git/inewave/.github/workflows/release.yml`.
- **mypy `strict` + `warn_return_any` interaction**: The ticket did not anticipate that enabling `strict = true` in `[[tool.mypy.overrides]]` re-enables `warn_return_any` even if it is set to `false` at the global `[tool.mypy]` level. The override block must explicitly repeat `warn_return_any = false`. Without this, mypy emits hundreds of errors across the codebase. File: `/home/rogerio/git/inewave/pyproject.toml`.
- **cfinterface 1.8.3 vs 1.9.0 conflict affects mypy globally**: `cfinterface>=1.9.0` is pinned as the runtime dependency but `cfinterface<=1.8.3` is the version that works without breaking the existing parsing model. This version conflict is not fully resolved in this epic. The mypy pre-commit hook was demoted to `stages: [manual]` as a direct consequence. This constraint will affect Epic 2 (Sphinx) if autodoc imports trigger the same conflict.

## Recommendations for Future Epics

- **Epic 2 (Sphinx modernization)**: When running `sphinx-build` with autodoc, Sphinx will import `inewave` — which will pull in `cfinterface`. Verify which cfinterface version is resolved in the docs virtualenv and whether autodoc succeeds. The `uv sync --extra docs` step in `/home/rogerio/git/inewave/.github/workflows/docs.yml` installs `cfinterface` as a transitive dependency; confirm the resolved version matches runtime expectations.
- **Before adding new CI steps**: All new checks should be added as separate parallel jobs following the pattern in `/home/rogerio/git/inewave/.github/workflows/main.yml`. Never add new steps to existing jobs — this preserves independent failure diagnostics.
- **Before using `exec()` to read Python metadata**: Prefer regex extraction over `exec()` for any `__init__.py` that has relative imports. The pattern established in `/home/rogerio/git/inewave/.github/workflows/release.yml` is the safe default.
- **When enabling mypy `strict` on new modules**: Always set `warn_return_any = false` explicitly in the `[[tool.mypy.overrides]]` block for that module, not just in `[tool.mypy]`. See `/home/rogerio/git/inewave/pyproject.toml` for the required structure.
- **Ruff per-file-ignores**: Any new directory with non-standard import ordering (e.g., tutorial scripts, benchmark scripts) should have its ignore rule added to the `per-file-ignores` table in `pyproject.toml` before running ruff for the first time to avoid noisy diffs.
