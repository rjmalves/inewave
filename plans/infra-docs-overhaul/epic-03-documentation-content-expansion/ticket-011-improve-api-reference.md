# ticket-011 Improve API Reference with Autosummary

## Context

### Background

The current API reference consists of manually maintained RST files under `docs/source/referencia/` — one RST file per class, each using `.. autoclass::` with `:members:`. While this approach works, it requires a new RST file for every new class added to the library, and the toctree in each module's `index.rst` must be manually updated. Sphinx's `autosummary` extension is already enabled in `conf.py` (`autosummary_generate = True`), but no autosummary directives are used in the actual reference pages. Adding autosummary tables to the module index pages will provide automatic summary tables of all classes while preserving the existing per-file detail pages.

### Relation to Epic

This is the fourth content-expansion ticket in Epic 3. It improves the existing API reference pages without removing current content. The changes will be integrated into the navigation by ticket-012.

### Current State

- `docs/source/conf.py` already has `sphinx.ext.autosummary` in extensions and `autosummary_generate = True`.
- `docs/source/_templates/layout.html` exists but contains old RTD-style CSS (leftover from Epic 2 theme migration — it uses `.wy-side-nav-search` and `.wy-nav-top` selectors that are RTD-specific and have no effect with Furo).
- Module index pages exist at:
  - `docs/source/referencia/newave/index.rst` — lists 65 files in toctree, no autosummary
  - `docs/source/referencia/nwlistop/index.rst` — lists 148 files in toctree, no autosummary
  - `docs/source/referencia/nwlistcf/index.rst` — lists 5 files in toctree, no autosummary
  - `docs/source/referencia/libs/index.rst` — lists 3 files in toctree, no autosummary
- Per-file RST pages use the pattern: `.. currentmodule::` + `.. autoclass:: ClassName` + `:members:`.
- Existing per-file RST pages must be preserved — they contain curated descriptions and register documentation (see `docs/source/referencia/libs/arquivos/eolica.rst` for an example with multiple `.. autoclass::` directives).
- numpydoc is used for docstring formatting (`numpydoc` in extensions, `numpydoc_show_class_members = False`).

## Specification

### Requirements

1. Add an `.. autosummary::` directive block to each of the 4 module index RST files, listing the public classes in that module. This creates a summary table at the top of each module reference page showing class names with one-line descriptions.
2. The autosummary blocks should use the `:nosignatures:` option (class constructors have complex signatures that clutter the summary table).
3. The autosummary blocks should NOT use `:toctree:` — the existing manual toctree entries already handle page generation. Adding `:toctree:` would create duplicate pages.
4. Add a brief introductory paragraph (in Portuguese) to each module index page above the autosummary block, explaining what the module contains.
5. Preserve all existing toctree entries — do NOT remove any per-file RST pages.
6. Clean up the stale `docs/source/_templates/layout.html` file that contains RTD-specific CSS rules (`.wy-side-nav-search`, `.wy-nav-top`, `.wy-menu-vertical`) that have no effect with Furo. Replace its content with a minimal template that only extends the base layout without RTD-specific overrides. Alternatively, if no custom layout is needed, the file can contain just `{% extends "!layout.html" %}`.
7. Do NOT create custom autosummary stub templates in `_templates/`.
8. Do NOT modify `docs/source/conf.py`.
9. Do NOT modify `docs/source/index.rst` — that is handled by ticket-012.
10. Do NOT modify any per-file RST pages under `referencia/*/arquivos/`.

### Inputs/Props

- The 4 module index RST files listed in Current State.
- The `inewave/newave/__init__.py` `_LAZY_IMPORTS` dict provides the list of public classes for the newave module (similarly for other subpackages).

### Outputs/Behavior

- Each module index page (`referencia/newave/index.rst`, `referencia/nwlistop/index.rst`, `referencia/nwlistcf/index.rst`, `referencia/libs/index.rst`) includes an `.. autosummary::` block listing all public classes.
- The autosummary blocks render as tables with class name and first-line docstring description.
- All existing toctree entries and per-file detail pages continue to work unchanged.
- `docs/source/_templates/layout.html` no longer contains RTD-specific CSS.

### Error Handling

- If a class listed in autosummary cannot be imported (e.g., due to cfinterface dependency issues), sphinx-build will emit a warning but should not fail. This is expected given the known cfinterface import issues.

## Acceptance Criteria

- [ ] Given the file `docs/source/referencia/newave/index.rst`, when inspecting its content, then it contains an `.. autosummary::` directive block listing at least 10 class names
- [ ] Given the file `docs/source/referencia/nwlistop/index.rst`, when inspecting its content, then it contains an `.. autosummary::` directive block listing at least 10 class names
- [ ] Given the file `docs/source/referencia/nwlistcf/index.rst`, when inspecting its content, then it contains an `.. autosummary::` directive block listing at least 3 class names
- [ ] Given the file `docs/source/referencia/libs/index.rst`, when inspecting its content, then it contains an `.. autosummary::` directive block listing at least 2 class names
- [ ] Given the 4 module index files, when inspecting their toctree directives, then all original toctree entries from the current state are preserved without removal or reordering

## Implementation Guide

### Suggested Approach

1. Read each subpackage's `__init__.py` to get the list of public class names from `_LAZY_IMPORTS`.
2. For each module index RST file:
   a. Add an introductory paragraph in Portuguese below the heading (e.g., "O modulo `inewave.newave` contem as classes para leitura e escrita dos arquivos de entrada e saida do modelo NEWAVE.").
   b. Add the `.. autosummary::` block with `:nosignatures:` option.
   c. List each public class using the fully qualified path (e.g., `inewave.newave.dger.Dger`), or set `.. currentmodule:: inewave.newave` above and use short names.
   d. Keep the existing `.. toctree::` block below the autosummary block, unchanged.
3. Clean up `docs/source/_templates/layout.html`:
   - Replace the content with just `{% extends "!layout.html" %}` since the RTD-specific CSS selectors have no effect in Furo.
4. Verify by running `sphinx-build -b html docs/source docs/build` that no new errors are introduced.

### Key Files to Modify

- `docs/source/referencia/newave/index.rst`
- `docs/source/referencia/nwlistop/index.rst`
- `docs/source/referencia/nwlistcf/index.rst`
- `docs/source/referencia/libs/index.rst`
- `docs/source/_templates/layout.html`

### Patterns to Follow

- Use `.. currentmodule::` before `.. autosummary::` to set the module context (same pattern used in per-file RST pages with `.. autoclass::`).
- Use `:nosignatures:` in autosummary to keep the table clean.

### Pitfalls to Avoid

- Do NOT add `:toctree:` to autosummary — it would create duplicate auto-generated stub pages that conflict with the existing manually curated per-file RST pages.
- Do NOT remove or reorder existing toctree entries — they must be preserved exactly as-is.
- Do NOT list internal/private classes (prefixed with `_`) in the autosummary blocks.
- Do NOT modify conf.py or any per-file RST pages under `arquivos/`.
- Some classes may fail to import due to cfinterface issues — this produces warnings, not errors.

## Testing Requirements

### Unit Tests

Not applicable — documentation-only ticket.

### Integration Tests

- Run `sphinx-build -b html docs/source docs/build` and verify:
  1. No new errors (warnings about cfinterface imports are acceptable).
  2. The autosummary tables appear in the generated HTML for each module index page.
  3. All existing per-file detail page links still work.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-006-migrate-sphinx-theme.md
- **Blocks**: ticket-012-update-index-toctree.md

## Effort Estimate

**Points**: 3
**Confidence**: High
