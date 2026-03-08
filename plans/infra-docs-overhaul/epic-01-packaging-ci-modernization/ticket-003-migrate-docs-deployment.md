# ticket-003 Migrate Docs Deployment to Official GitHub Pages Actions

## Context

### Background

The current docs deployment workflow at `.github/workflows/docs.yml` uses `peaceiris/actions-gh-pages@v3`, a third-party action that is no longer actively maintained and has been superseded by GitHub's official Pages deployment actions. The official approach uses `actions/upload-pages-artifact` to create an artifact and `actions/deploy-pages` to deploy it, providing better security (no personal access tokens needed), official support, and integration with GitHub's deployment environment UI.

### Relation to Epic

This is the third ticket in Epic 1. It modernizes the documentation deployment pipeline, which Epic 2 (Sphinx theme migration) depends on for validating that the new Furo theme deploys correctly.

### Current State

The file at `/home/rogerio/git/inewave/.github/workflows/docs.yml`:

- Triggered on push to `main` and `workflow_dispatch`
- Single job `docs` that: installs uv, syncs deps, runs pytest (redundant), runs sphinx-build, then deploys with `peaceiris/actions-gh-pages@v3`
- The deploy step uses `github_token: ${{ secrets.GITHUB_TOKEN }}`, publishes to `gh-pages` branch, uses `force_orphan: true`
- Runs pytest redundantly (tests already run in `main.yml`)

## Specification

### Requirements

1. Replace `peaceiris/actions-gh-pages@v3` with official GitHub Pages deployment:
   - `actions/upload-pages-artifact@v3` to upload the built docs
   - `actions/deploy-pages@v4` to deploy to GitHub Pages
2. Add proper `permissions` block: `pages: write`, `id-token: write`
3. Add `environment` configuration pointing to `github-pages`
4. Remove the redundant `pytest` step (tests are already run by `main.yml`)
5. Keep the `workflow_dispatch` trigger for manual deployments
6. Use `concurrency` group to prevent concurrent deployments

### Inputs/Props

- File: `/home/rogerio/git/inewave/.github/workflows/docs.yml`

### Outputs/Behavior

- Documentation builds and deploys to GitHub Pages on push to `main`
- Deployment is visible in the repository's Environments tab
- The `gh-pages` branch is no longer needed (official Pages deploy uses artifacts, not branches)

### Error Handling

- If sphinx-build fails, the workflow should fail before the upload/deploy steps
- If deployment fails, the error should be visible in the Actions UI with a clear error message

## Acceptance Criteria

- [ ] Given the updated `docs.yml`, when searching for `peaceiris/actions-gh-pages`, then no match is found in the file
- [ ] Given the updated `docs.yml`, when reading the deploy step, then it uses `actions/deploy-pages@v4`
- [ ] Given the updated `docs.yml`, when reading the job permissions, then `pages: write` and `id-token: write` are present
- [ ] Given the updated `docs.yml`, when searching for `pytest`, then no match is found (redundant test step removed)
- [ ] Given the updated `docs.yml`, when reading the workflow triggers, then both `push: branches: [main]` and `workflow_dispatch` are present

## Implementation Guide

### Suggested Approach

1. Open `/home/rogerio/git/inewave/.github/workflows/docs.yml`
2. Replace the entire file with:

   ```yaml
   name: Docs

   on:
     push:
       branches:
         - main
     workflow_dispatch:

   permissions:
     pages: write
     id-token: write

   concurrency:
     group: "pages"
     cancel-in-progress: false

   jobs:
     docs:
       runs-on: ubuntu-latest
       environment:
         name: github-pages
         url: ${{ steps.deploy.outputs.page_url }}
       steps:
         - uses: actions/checkout@v4
         - name: Install uv
           uses: astral-sh/setup-uv@v3
         - name: Set up Python
           run: uv python install 3.12
         - name: Install the project
           run: uv sync --extra docs
         - name: Sphinx build
           run: uv run sphinx-build -M html docs/source docs/build
         - name: Upload artifact
           uses: actions/upload-pages-artifact@v3
           with:
             path: docs/build/html
         - name: Deploy to GitHub Pages
           id: deploy
           uses: actions/deploy-pages@v4
   ```

3. Note: After this migration, the GitHub Pages source in repository Settings > Pages should be set to "GitHub Actions" (not "Deploy from a branch").

### Key Files to Modify

- `/home/rogerio/git/inewave/.github/workflows/docs.yml`

### Patterns to Follow

- Use the official `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4` pattern recommended by GitHub
- Use `concurrency` group to prevent concurrent deployments from conflicting
- Use `--extra docs` to install only documentation dependencies

### Pitfalls to Avoid

- Do NOT keep the `pytest` step in the docs workflow. Tests are validated by `main.yml`. Running them again in the docs workflow wastes CI time.
- Do NOT forget to configure the repository's Pages settings to use "GitHub Actions" as the source. Without this, the `deploy-pages` action will fail with a permissions error.
- Do NOT use `actions/configure-pages` unless needed. For simple deployments, `upload-pages-artifact` + `deploy-pages` is sufficient.
- The `uv sync --extra docs` command will also install the main package dependencies (numpy, pandas, cfinterface) since Sphinx needs to import the package for autodoc.

## Testing Requirements

### Unit Tests

- Not applicable (CI configuration change)

### Integration Tests

- Push the branch to GitHub and trigger a manual docs deployment via `workflow_dispatch`
- Verify the deployment appears in the repository's Environments tab
- Verify the documentation site is accessible at `https://rjmalves.github.io/inewave/`

### E2E Tests

- Not applicable

## Dependencies

- **Blocked By**: ticket-001-modernize-pyproject-toml.md (needs the `docs` dependency group)
- **Blocks**: ticket-006-migrate-sphinx-theme.md (Epic 2, theme migration should use the new deployment pipeline)

## Effort Estimate

**Points**: 2
**Confidence**: High
