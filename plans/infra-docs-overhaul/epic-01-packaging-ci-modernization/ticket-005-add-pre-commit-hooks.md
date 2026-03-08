# ticket-005 Add Pre-commit Hooks for Ruff and Mypy

## Context

### Background

The project currently has no pre-commit hook configuration. Developers can push code that fails ruff linting or mypy type checking, only to discover the failure in CI minutes later. Pre-commit hooks catch these issues locally before the code is committed, providing faster feedback and reducing CI failures.

### Relation to Epic

This is the fifth and final ticket in Epic 1. It completes the developer tooling modernization by adding local hooks that mirror the CI checks.

### Current State

- No `.pre-commit-config.yaml` file exists in the repository root
- ruff is configured in `pyproject.toml` with `line-length = 80`
- mypy is configured in `pyproject.toml` with strict mode for all submodules
- Both tools are already in the `lint` dependency group (from ticket-001)

## Specification

### Requirements

1. Create `.pre-commit-config.yaml` in the repository root with hooks for:
   - **ruff**: Using the official `astral-sh/ruff-pre-commit` mirror for both `ruff check` (linting) and `ruff format --check` (formatting)
   - **mypy**: Using a `local` hook that runs `mypy ./inewave` (mypy needs the project installed to resolve imports, so a mirrored hook is not suitable)
2. Pin hook versions to current stable releases (ruff v0.9.x or latest, mypy to the version in the project's dev deps)
3. Add `pre-commit` to the `lint` dependency group in `pyproject.toml`
4. Verify that `pre-commit run --all-files` passes cleanly

### Inputs/Props

- New file: `/home/rogerio/git/inewave/.pre-commit-config.yaml`
- Modify: `/home/rogerio/git/inewave/pyproject.toml` (add `pre-commit` to lint deps)

### Outputs/Behavior

- Running `pre-commit install` sets up the git hook
- Running `pre-commit run --all-files` executes ruff and mypy checks on all files
- Committing code with ruff or mypy violations is blocked by the hook

### Error Handling

- If mypy is slow on the full codebase, the hook should still work but may be slow. This is acceptable for commit-time checks. Developers can use `--no-verify` to bypass in exceptional cases.

## Acceptance Criteria

- [ ] Given the repository root, when listing files, then `.pre-commit-config.yaml` exists
- [ ] Given the `.pre-commit-config.yaml`, when reading the hooks, then there is a `ruff` hook from `astral-sh/ruff-pre-commit` with both `ruff-check` and `ruff-format` hook IDs
- [ ] Given the `.pre-commit-config.yaml`, when reading the hooks, then there is a `mypy` hook configured as a `local` hook running `mypy ./inewave`
- [ ] Given the updated `pyproject.toml`, when reading the `lint` dependency group, then `pre-commit` is listed as a dependency
- [ ] Given a clean working tree, when running `pre-commit run --all-files`, then all hooks pass with exit code 0

## Implementation Guide

### Suggested Approach

1. Create `/home/rogerio/git/inewave/.pre-commit-config.yaml`:

   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.9.7
       hooks:
         - id: ruff
           args: [--fix]
         - id: ruff-format

     - repo: local
       hooks:
         - id: mypy
           name: mypy
           entry: uv run mypy ./inewave
           language: system
           types: [python]
           pass_filenames: false
   ```

2. Update `/home/rogerio/git/inewave/pyproject.toml` to add `pre-commit` to the `lint` group:
   ```toml
   lint = [
       "ruff",
       "mypy",
       "pre-commit",
   ]
   ```
3. Run `uv sync --extra lint` to install pre-commit
4. Run `pre-commit install` to set up the git hook
5. Run `pre-commit run --all-files` to verify all hooks pass
6. Check the latest ruff-pre-commit release version and update `rev` accordingly

### Key Files to Modify

- `/home/rogerio/git/inewave/.pre-commit-config.yaml` (create)
- `/home/rogerio/git/inewave/pyproject.toml` (add `pre-commit` to lint deps)

### Patterns to Follow

- Use the official `astral-sh/ruff-pre-commit` mirror for ruff hooks (faster than running through pip)
- Use `local` repo type for mypy since it requires the project to be installed in the environment
- Use `pass_filenames: false` for the mypy hook to run on the entire package (mypy needs full-project analysis for strict mode)
- Use `language: system` for the mypy hook so it uses the project's virtualenv

### Pitfalls to Avoid

- Do NOT use a mirrored mypy hook (e.g., `mirrors-mypy`). mypy needs the project and its dependencies installed to resolve imports. Using a mirrored hook would create an isolated environment without the project's dependencies, causing import errors.
- The ruff `--fix` argument in the ruff hook means it will auto-fix fixable issues. If this is undesirable, remove `args: [--fix]`. However, auto-fix is generally preferred for pre-commit hooks.
- Do NOT add `ruff format` as a check-only hook AND a fix hook. Use either `ruff-format` (which formats in-place) or `ruff-format` with `args: [--check]` (which only checks). The standard pattern is to format in-place.
- Pin the `rev` to a specific version tag, not `main` or a commit hash.

## Testing Requirements

### Unit Tests

- Not applicable (configuration file change)

### Integration Tests

- Run `pre-commit run --all-files` and verify exit code 0
- Verify ruff hook catches a deliberate lint violation (create a temp file with unused import, run pre-commit, verify it flags or fixes it)

### E2E Tests

- Not applicable

## Dependencies

- **Blocked By**: ticket-001-modernize-pyproject-toml.md (needs the `lint` dependency group to add `pre-commit` to)
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High
