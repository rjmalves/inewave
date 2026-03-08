# ticket-001 Modernize pyproject.toml Metadata and Wheel Configuration

## Context

### Background

The `pyproject.toml` file is the single source of truth for project metadata, build configuration, and developer tooling. The current configuration is functional but has several gaps: missing Python 3.11/3.12 classifiers, the `py.typed` marker file exists at `inewave/py.typed` but is not explicitly included in the wheel build targets, the project description is a bare "inewave" instead of a meaningful sentence, and there is a local `cfinterface` source override in `[tool.uv.sources]` that should not be present in the committed file.

### Relation to Epic

This is the first ticket in Epic 1 (Packaging & CI Modernization). It establishes the correct project metadata foundation that the CI workflows and release process depend on.

### Current State

The file at `/home/rogerio/git/inewave/pyproject.toml` currently has:

- `description = "inewave"` (not descriptive)
- Classifiers include only `Programming Language :: Python :: 3.10`, missing 3.11 and 3.12
- Missing `Typing :: Typed` classifier despite `py.typed` existing
- `[tool.hatch.build.targets.wheel]` includes only `inewave/` but does not explicitly ensure `py.typed` is bundled
- `[tool.uv.sources]` contains `cfinterface = { path = "/home/rogerio/git/cfinterface" }` (local dev override)
- Dev dependencies are a flat list mixing testing, linting, typing, and documentation tools

## Specification

### Requirements

1. Update `description` to a meaningful Portuguese sentence: `"Pacote Python para manipulação dos arquivos de entrada e saída do NEWAVE"`
2. Add missing classifiers: `Programming Language :: Python :: 3.11`, `Programming Language :: Python :: 3.12`, `Typing :: Typed`
3. Remove the `[tool.uv.sources]` section entirely (local dev override should not be committed)
4. Split `[project.optional-dependencies]` into logical groups:
   - `dev` (or `test`): pytest, pytest-cov, pytest-xdist
   - `lint`: ruff, mypy
   - `docs`: sphinx, sphinx-gallery, numpydoc, plotly, matplotlib, and the theme package (currently sphinx-rtd-theme, will be furo after Epic 2)
5. Verify `py.typed` is included in the wheel by checking that the `include` pattern `"inewave/"` captures it (it does since `py.typed` is inside `inewave/`)

### Inputs/Props

- File: `/home/rogerio/git/inewave/pyproject.toml`
- File: `/home/rogerio/git/inewave/inewave/py.typed` (exists, empty marker file)

### Outputs/Behavior

- Updated `pyproject.toml` with all changes above
- Running `uv build` produces a wheel that contains `inewave/py.typed`

### Error Handling

- If `uv build` fails after changes, the classifiers or dependency syntax is incorrect and must be fixed before the ticket is considered complete.

## Acceptance Criteria

- [ ] Given the updated `pyproject.toml`, when reading the `[project]` section, then `description` contains `"Pacote Python para manipulação dos arquivos de entrada e saída do NEWAVE"`
- [ ] Given the updated `pyproject.toml`, when reading the `classifiers` list, then it contains `"Programming Language :: Python :: 3.11"`, `"Programming Language :: Python :: 3.12"`, and `"Typing :: Typed"`
- [ ] Given the updated `pyproject.toml`, when searching for `[tool.uv.sources]`, then the section does not exist in the file
- [ ] Given the updated `pyproject.toml`, when reading `[project.optional-dependencies]`, then dependencies are split into at least `test`, `lint`, and `docs` groups
- [ ] Given the updated `pyproject.toml`, when running `uv build && unzip -l dist/*.whl | grep py.typed`, then the output shows `inewave/py.typed` is present in the wheel

## Implementation Guide

### Suggested Approach

1. Open `/home/rogerio/git/inewave/pyproject.toml`
2. Update the `description` field value
3. Add the three missing classifiers to the `classifiers` list
4. Replace the single `dev` optional-dependency group with three groups:
   ```toml
   [project.optional-dependencies]
   test = [
       "pytest",
       "pytest-cov",
       "pytest-xdist",
   ]
   lint = [
       "ruff",
       "mypy",
   ]
   docs = [
       "sphinx",
       "sphinx-rtd-theme",
       "sphinx-gallery",
       "numpydoc",
       "plotly",
       "matplotlib",
   ]
   dev = [
       "inewave[test,lint,docs]",
   ]
   ```
5. Remove the entire `[tool.uv.sources]` section at the bottom of the file
6. Run `uv sync --all-extras --dev` to verify dependencies resolve correctly
7. Run `uv build` and inspect the wheel contents for `py.typed`

### Key Files to Modify

- `/home/rogerio/git/inewave/pyproject.toml`

### Patterns to Follow

- Use self-referencing extras (`"inewave[test,lint,docs]"`) for the `dev` group so that `uv sync --all-extras --dev` still installs everything
- Keep alphabetical ordering within each dependency group

### Pitfalls to Avoid

- Do NOT remove the `[tool.uv.sources]` section from the user's local working copy in a way that breaks their development workflow. The change is for the committed file. The user can re-add it locally via `uv` overrides.
- Do NOT change the `[tool.hatch.build.targets.wheel]` include pattern. The current `"inewave/"` glob already captures `py.typed` since it is inside the `inewave/` directory.
- Do NOT modify `[tool.mypy]`, `[tool.pytest.ini_options]`, or `[tool.ruff]` sections. Those are already configured correctly.

## Testing Requirements

### Unit Tests

- Not applicable (configuration file change)

### Integration Tests

- Run `uv sync --all-extras --dev` to verify dependency resolution
- Run `uv build` to verify the package builds successfully
- Inspect wheel contents to verify `py.typed` is included

### E2E Tests

- Not applicable

## Dependencies

- **Blocked By**: None
- **Blocks**: ticket-002-restructure-ci-workflow.md (CI workflow references dependency groups)

## Effort Estimate

**Points**: 2
**Confidence**: High
