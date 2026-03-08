# ticket-004 Create Release Workflow with Trusted Publishing

## Context

### Background

The current publish workflow at `.github/workflows/publish.yml` is triggered by GitHub release events (`on: release: types: [created]`). While it already uses trusted publishing (OIDC via `pypa/gh-action-pypi-publish@release/v1`), it has several issues: it runs tests and type checking redundantly (these should pass on `main` before a release is created), and it triggers on release creation which requires manual GitHub UI interaction. A more robust approach triggers on version tag pushes (`v*`), validates the tag matches the package version, and skips redundant checks.

### Relation to Epic

This is the fourth ticket in Epic 1. It replaces the existing release workflow with a cleaner, more reliable publishing pipeline.

### Current State

The file at `/home/rogerio/git/inewave/.github/workflows/publish.yml`:

- Named `deploy`, triggered on `release: types: [created]`
- Single job `build-and-publish` with environment `pypi` and `id-token: write` permissions
- Steps: checkout, uv install, python 3.12, uv sync, pytest, mypy, ruff, uv build (conditional on tag), pypi publish (conditional on tag)
- The tag-conditional steps use `if: startsWith(github.ref, 'refs/tags')`

## Specification

### Requirements

1. Rename the workflow file from `publish.yml` to `release.yml` for clarity
2. Change trigger from `release: types: [created]` to `push: tags: ["v*"]`
3. Remove redundant test, mypy, and ruff steps (these are guaranteed by CI on `main`)
4. Add a version validation step that extracts the version from `inewave/__init__.py` and compares it to the git tag
5. Keep the trusted publishing setup: environment `pypi`, `id-token: write`, `pypa/gh-action-pypi-publish@release/v1`
6. Add a step to create a GitHub release from the tag using `gh release create`

### Inputs/Props

- File: `/home/rogerio/git/inewave/.github/workflows/publish.yml` (to be renamed to `release.yml`)
- File: `/home/rogerio/git/inewave/inewave/__init__.py` (contains `__version__`)

### Outputs/Behavior

- Pushing a tag like `v1.13.0` triggers the workflow
- Workflow validates that the tag `v1.13.0` matches `__version__ = "1.13.0"` in `inewave/__init__.py`
- If validation passes, builds the package and publishes to PyPI
- Creates a GitHub release for the tag

### Error Handling

- If version tag does not match `__version__`, the workflow fails with a clear error message before building or publishing
- If PyPI publish fails, the error is visible in the Actions UI

## Acceptance Criteria

- [ ] Given the workflows directory, when listing files, then `release.yml` exists and `publish.yml` does not exist
- [ ] Given the `release.yml`, when reading the trigger, then it is `push: tags: ["v*"]` and not `release: types: [created]`
- [ ] Given the `release.yml`, when searching for `pytest`, `mypy`, or `ruff`, then no matches are found (redundant checks removed)
- [ ] Given the `release.yml`, when reading the steps, then there is a version validation step that compares the git tag to `__version__` in `inewave/__init__.py`
- [ ] Given the `release.yml`, when reading the publish step, then it uses `pypa/gh-action-pypi-publish@release/v1` with `id-token: write` permissions

## Implementation Guide

### Suggested Approach

1. Delete `/home/rogerio/git/inewave/.github/workflows/publish.yml`
2. Create `/home/rogerio/git/inewave/.github/workflows/release.yml` with:

   ```yaml
   name: Release

   on:
     push:
       tags:
         - "v*"

   jobs:
     release:
       runs-on: ubuntu-latest
       environment:
         name: pypi
         url: https://pypi.org/p/inewave
       permissions:
         contents: write
         id-token: write
       steps:
         - uses: actions/checkout@v4
         - name: Install uv
           uses: astral-sh/setup-uv@v3
         - name: Set up Python
           run: uv python install 3.12
         - name: Validate version matches tag
           run: |
             TAG_VERSION="${GITHUB_REF#refs/tags/v}"
             PKG_VERSION=$(python -c "exec(open('inewave/__init__.py').read()); print(__version__)")
             if [ "$TAG_VERSION" != "$PKG_VERSION" ]; then
               echo "::error::Tag version ($TAG_VERSION) does not match package version ($PKG_VERSION)"
               exit 1
             fi
         - name: Install the project
           run: uv sync
         - name: Build package
           run: uv build
         - name: Publish to PyPI
           uses: pypa/gh-action-pypi-publish@release/v1
         - name: Create GitHub Release
           env:
             GH_TOKEN: ${{ github.token }}
           run: gh release create "$GITHUB_REF_NAME" dist/* --generate-notes
   ```

3. The `contents: write` permission is needed for `gh release create`

### Key Files to Modify

- `/home/rogerio/git/inewave/.github/workflows/publish.yml` (delete)
- `/home/rogerio/git/inewave/.github/workflows/release.yml` (create)

### Patterns to Follow

- Use tag-triggered workflows for releases instead of release-event triggers
- Validate version consistency between tag and source code before publishing
- Use `gh release create` with `--generate-notes` for automatic release notes generation

### Pitfalls to Avoid

- Do NOT keep `publish.yml` alongside `release.yml`. Delete the old file to avoid confusion.
- The version extraction step must handle the `__version__` format in `inewave/__init__.py` correctly. The current format is `__version__ = "1.13.0"` with surrounding docstring and imports.
- Do NOT add pytest/mypy/ruff steps. These should have already passed on the `main` branch CI before a version tag is created.
- The `contents: write` permission is required for `gh release create`. Without it, the step will fail with a 403 error.

## Testing Requirements

### Unit Tests

- Not applicable (CI configuration change)

### Integration Tests

- Verify the YAML syntax is valid
- Verify the version extraction command works locally: `python -c "exec(open('inewave/__init__.py').read()); print(__version__)"`

### E2E Tests

- Full validation requires pushing a version tag, which should only be done during an actual release

## Dependencies

- **Blocked By**: ticket-001-modernize-pyproject-toml.md (needs clean pyproject.toml)
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High
