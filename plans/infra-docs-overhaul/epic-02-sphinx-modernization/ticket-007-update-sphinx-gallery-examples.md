# ticket-007 Update Sphinx-gallery Examples for Current API Patterns

## Context

### Background

The inewave project has 21 sphinx-gallery example scripts in `/home/rogerio/git/inewave/examples/` that demonstrate reading and visualizing various NEWAVE files using matplotlib and plotly. These examples may use deprecated API patterns (e.g., the old `set_version()` approach instead of the new `version=` parameter) or reference deprecated classes. They need to be reviewed and updated to reflect the current v1.13.0 API, and verified to build cleanly with sphinx-gallery under the Furo theme.

### Relation to Epic

This is the second and final ticket in Epic 2. It ensures the example gallery is up-to-date and builds cleanly with the new Furo theme.

### Current State

The examples directory at `/home/rogerio/git/inewave/examples/` contains:

- `README.txt` (gallery description)
- `__init__.py`
- 19 `plot_*.py` scripts covering: confhd, cortes, dger, energiaf, forward, hidr, manutt, modif, patamar, penalid, pmo, polinjus, ree, restricoes_eletricas, sistema, term, vazaof, versionamento
- Subdirectories: `libs/`, `newave/`, `nwlistop/` (additional examples organized by module)

The sphinx-gallery configuration in `conf.py`:

```python
sphinx_gallery_conf = {
    "examples_dirs": "../../examples",
    "gallery_dirs": "examples",
    "backreferences_dir": "gen_modules/generated",
}
```

## Specification

### Requirements

1. Review each `plot_*.py` example script for:
   - Use of deprecated classes (`ValoresSerie`, `ValoresSeriePatamar`, `AvlCortesFpha`)
   - Use of old `set_version()` pattern instead of `version=` parameter
   - References to old file class names (pre-v1.8.0 renames)
   - Outdated import paths
2. Update any examples using deprecated patterns to use the current API
3. Verify each example script can be executed standalone (produces a plot without errors)
4. Verify sphinx-gallery builds all examples without errors
5. Update `README.txt` if the gallery description is outdated

### Inputs/Props

- Directory: `/home/rogerio/git/inewave/examples/`
- File: `/home/rogerio/git/inewave/docs/source/conf.py` (sphinx-gallery config)

### Outputs/Behavior

- All example scripts use current v1.13.0 API patterns
- No deprecated class references in examples
- sphinx-gallery builds all examples without errors or warnings
- Generated gallery pages display correctly with Furo theme

### Error Handling

- If an example requires mock data files that are not available in the repository, document the required files in a comment at the top of the script or skip the example from the gallery build using sphinx-gallery's `ignore_pattern` configuration.

## Acceptance Criteria

- [ ] Given the examples directory, when searching all `plot_*.py` files for `set_version`, then no matches are found (old pattern replaced with `version=` parameter)
- [ ] Given the examples directory, when searching all `plot_*.py` files for `ValoresSerie` or `ValoresSeriePatamar`, then no matches are found (deprecated classes replaced)
- [ ] Given the updated examples, when running `uv run sphinx-build -M html docs/source docs/build`, then sphinx-gallery builds all examples without errors
- [ ] Given the built documentation, when navigating to the examples gallery page, then all example thumbnails and pages render correctly with the Furo theme

## Implementation Guide

### Suggested Approach

1. Read each `plot_*.py` file in `/home/rogerio/git/inewave/examples/`
2. For each file, check for:
   - `set_version(` calls -- replace with `version=` parameter in the `read()` call
   - Imports of `ValoresSerie` or `ValoresSeriePatamar` -- replace with `TabelaSerieAnual` or `TabelaSeriePatamarAnual` if directly referenced
   - Imports of old class names (e.g., `AvlCortesFpha`) -- replace with new names (e.g., `FphaCortes`)
   - Any `from inewave` import that no longer resolves
3. Also check the subdirectories (`examples/libs/`, `examples/newave/`, `examples/nwlistop/`) for additional example scripts
4. Run `uv run sphinx-build -M html docs/source docs/build` and check for sphinx-gallery errors
5. Review the generated gallery pages in `docs/build/html/examples/` for correct rendering

### Key Files to Modify

- `/home/rogerio/git/inewave/examples/plot_*.py` (up to 19 files, only those needing changes)
- `/home/rogerio/git/inewave/examples/README.txt` (if outdated)
- Files in `/home/rogerio/git/inewave/examples/libs/`, `examples/newave/`, `examples/nwlistop/` (if they exist and need updates)

### Patterns to Follow

- Use `Classe.read("./arquivo.ext", version="XX")` instead of `Classe.set_version("XX"); Classe.read("./arquivo.ext")`
- Use current class names from the v1.13.0 API
- Keep all example docstrings in Brazilian Portuguese

### Pitfalls to Avoid

- Do NOT change the sphinx-gallery configuration in `conf.py` unless there is a build error that requires it
- Some examples may require specific mock data files. If those files are missing, the example will fail during sphinx-gallery build. Check if mock data exists before assuming the example should build.
- Do NOT add new examples in this ticket. New examples belong in Epic 3 if needed.
- The `plot_versionamento.py` example specifically demonstrates versioning -- make sure it uses the new `version=` parameter pattern.

## Testing Requirements

### Unit Tests

- Not applicable (documentation examples)

### Integration Tests

- Run `uv run sphinx-build -M html docs/source docs/build` and verify sphinx-gallery section completes without errors
- Visually inspect at least 5 gallery pages in the built documentation

### E2E Tests

- Not applicable

## Dependencies

- **Blocked By**: ticket-006-migrate-sphinx-theme.md (examples should be tested with Furo theme)
- **Blocks**: None directly, but Epic 3 documentation content may reference examples

## Effort Estimate

**Points**: 2
**Confidence**: Medium (depends on how many examples need changes and whether mock data is available)
