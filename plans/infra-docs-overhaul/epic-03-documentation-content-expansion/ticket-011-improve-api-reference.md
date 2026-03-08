# ticket-011 Improve API Reference with Autosummary

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Improve the API reference documentation by leveraging Sphinx autosummary to automatically generate comprehensive module and class documentation pages for all public modules in inewave. The current reference pages are manually maintained RST files that may become stale as the library evolves. Autosummary ensures the reference always matches the source code.

## Anticipated Scope

- **Files likely to be modified**: `docs/source/referencia/newave/index.rst`, `docs/source/referencia/nwlistop/index.rst`, `docs/source/referencia/nwlistcf/index.rst`, `docs/source/referencia/libs/index.rst`, `docs/source/conf.py` (autosummary templates), `docs/source/_templates/` (autosummary templates)
- **Key decisions needed**: Whether to replace the current manual RST files entirely with autosummary-generated pages or supplement them; whether to create custom autosummary templates; how to handle deprecated classes in the generated reference
- **Open questions**: Should autosummary generate pages for internal modules (prefixed with `_`)? How should versioned classes (VERSIONS dict) be documented? Should the existing per-file RST pages in `referencia/newave/arquivos/` be preserved alongside autosummary?

## Dependencies

- **Blocked By**: ticket-006-migrate-sphinx-theme.md
- **Blocks**: ticket-012-update-index-toctree.md

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
