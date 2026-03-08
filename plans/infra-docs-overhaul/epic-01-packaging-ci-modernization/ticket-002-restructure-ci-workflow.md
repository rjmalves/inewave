# ticket-002 Restructure CI Workflow into Parallel Jobs

## Context

### Background

The current CI workflow at `.github/workflows/main.yml` runs all checks (pytest, mypy, ruff, sphinx-build) sequentially within a single job across a Python version matrix. This means a ruff formatting error is only detected after tests complete, and a documentation build failure is only caught last. Parallel jobs provide faster feedback and clearer failure diagnostics.

### Relation to Epic

This is the second ticket in Epic 1. It restructures the main CI pipeline to run lint, typecheck, test, and docs as independent parallel jobs.

### Current State

The file at `/home/rogerio/git/inewave/.github/workflows/main.yml`:

- Named `tests`, triggered on push/PR to `main`
- Single job `test` with matrix `python-version: ["3.10", "3.11", "3.12"]`
- Steps run sequentially: checkout -> uv install -> uv sync -> pytest with codecov -> mypy -> ruff -> sphinx-build
- Uses `astral-sh/setup-uv@v3`, `actions/checkout@v4`, `codecov/codecov-action@v4`

## Specification

### Requirements

1. Replace the single `test` job with four parallel jobs: `lint`, `typecheck`, `test`, `docs`
2. **`lint` job**: Runs on a single Python version (3.12), installs only lint deps, runs `ruff check ./inewave`
3. **`typecheck` job**: Runs on a single Python version (3.12), installs lint deps (mypy is there), runs `mypy ./inewave`
4. **`test` job**: Runs on Python matrix [3.10, 3.11, 3.12], installs test deps, runs `pytest --cov-report=xml --cov=inewave ./tests`, uploads to codecov
5. **`docs` job**: Runs on a single Python version (3.12), installs docs deps, runs `sphinx-build -M html docs/source docs/build`
6. All jobs use `astral-sh/setup-uv@v3` and `actions/checkout@v4`
7. Each job installs only the dependency group it needs (using the split groups from ticket-001)

### Inputs/Props

- File: `/home/rogerio/git/inewave/.github/workflows/main.yml`
- Dependency groups from ticket-001: `test`, `lint`, `docs`

### Outputs/Behavior

- Four independent jobs visible in GitHub Actions UI
- Each job fails independently without blocking others
- Total wall-clock time reduced (parallel execution)

### Error Handling

- If any individual job fails, the overall workflow status is "failed" but other jobs continue running
- Codecov upload failure should not fail the test job (set `fail_ci_if_error: false` or keep `true` per current config)

## Acceptance Criteria

- [ ] Given the updated `main.yml`, when a push to `main` triggers the workflow, then four separate jobs appear in the GitHub Actions UI: `lint`, `typecheck`, `test`, `docs`
- [ ] Given the `lint` job definition, when reading its steps, then it runs only `ruff check ./inewave` and does not run pytest, mypy, or sphinx-build
- [ ] Given the `typecheck` job definition, when reading its steps, then it runs only `mypy ./inewave` and does not run pytest, ruff, or sphinx-build
- [ ] Given the `test` job definition, when reading its steps, then it uses a Python version matrix of `["3.10", "3.11", "3.12"]` and runs `pytest --cov-report=xml --cov=inewave ./tests`
- [ ] Given the `docs` job definition, when reading its steps, then it runs `sphinx-build -M html docs/source docs/build` on Python 3.12

## Implementation Guide

### Suggested Approach

1. Open `/home/rogerio/git/inewave/.github/workflows/main.yml`
2. Rename the workflow from `tests` to `CI` (or `ci`)
3. Replace the single `test` job with four jobs. Each job follows this pattern:

   ```yaml
   jobs:
     lint:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v3
         - run: uv python install 3.12
         - run: uv sync --extra lint
         - run: uv run ruff check ./inewave

     typecheck:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v3
         - run: uv python install 3.12
         - run: uv sync --extra lint
         - run: uv run mypy ./inewave

     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: ["3.10", "3.11", "3.12"]
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v3
         - run: uv python install ${{ matrix.python-version }}
         - run: uv sync --extra test
         - run: uv run pytest --cov-report=xml --cov=inewave ./tests
         - uses: codecov/codecov-action@v4
           with:
             token: ${{ secrets.CODECOV_TOKEN }}
             files: ./coverage.xml
             flags: unittests
             env_vars: OS,PYTHON
             name: codecov-inewave
             fail_ci_if_error: true
             verbose: true

     docs:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v3
         - run: uv python install 3.12
         - run: uv sync --extra docs
         - run: uv run sphinx-build -M html docs/source docs/build
   ```

4. Verify the workflow YAML is valid
5. Note: the `test` job needs `uv sync --extra test` but mypy/ruff are in `lint`, and sphinx in `docs`. Each job installs only what it needs.

### Key Files to Modify

- `/home/rogerio/git/inewave/.github/workflows/main.yml`

### Patterns to Follow

- Use `uv sync --extra <group>` to install only the dependency group needed by each job
- Keep the `actions/checkout@v4` and `astral-sh/setup-uv@v3` versions consistent across all jobs
- Use named steps with descriptive names (e.g., `name: Run ruff linter`)

### Pitfalls to Avoid

- Do NOT add `needs:` dependencies between the four jobs. They should run in parallel, not sequentially.
- The `typecheck` job needs the main package installed (mypy analyzes `./inewave`), so `uv sync --extra lint` is sufficient because it installs the package plus lint extras.
- Do NOT remove the codecov step from the test job. Keep the existing codecov configuration.
- Verify that `uv sync --extra test` installs `numpy`, `pandas`, and `cfinterface` (they are main dependencies, not extras, so they will be installed regardless of which extra group is selected).

## Testing Requirements

### Unit Tests

- Not applicable (CI configuration change)

### Integration Tests

- Push the branch to GitHub and verify all four jobs appear and run in the Actions UI
- Verify each job installs only its required dependencies (check job logs)

### E2E Tests

- Not applicable

## Dependencies

- **Blocked By**: ticket-001-modernize-pyproject-toml.md (dependency groups must exist in pyproject.toml)
- **Blocks**: None directly, but ticket-003 modifies the docs workflow separately

## Effort Estimate

**Points**: 3
**Confidence**: High
