# Epic 2: Sphinx Modernization

## Goals

Migrate the documentation infrastructure from the legacy `sphinx-rtd-theme` to the modern Furo theme, and update sphinx-gallery examples to ensure they build cleanly and reflect current library usage patterns.

## Scope

- Replace `sphinx-rtd-theme` with Furo in Sphinx configuration and dependencies
- Update `conf.py` theme options, remove RTD-specific configuration
- Update sphinx-gallery examples to ensure they build without errors and use current API patterns
- Verify intersphinx mappings and all existing documentation pages render correctly with Furo

## Out of Scope

- Writing new documentation pages (that is Epic 3)
- Migrating from pandas to Polars in examples (inewave uses pandas)
- Modifying library source code
- Changing the documentation language

## Tickets

| Ticket     | Title                                                   | Effort |
| ---------- | ------------------------------------------------------- | ------ |
| ticket-006 | Migrate Sphinx theme from sphinx-rtd-theme to Furo      | 3      |
| ticket-007 | Update sphinx-gallery examples for current API patterns | 2      |

## Dependencies

- **Blocked By**: Epic 1 (ticket-003 specifically, for the updated docs deployment pipeline)
- Epic 3 depends on this epic completing first (new content should be written for the Furo theme)

## Acceptance Criteria

- `sphinx-build` completes without errors or warnings using Furo theme
- All existing documentation pages render correctly (visual inspection)
- All sphinx-gallery examples build and produce expected output
- Dark mode toggle works in the built documentation
