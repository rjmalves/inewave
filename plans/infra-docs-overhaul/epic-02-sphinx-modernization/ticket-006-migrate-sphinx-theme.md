# ticket-006 Migrate Sphinx Theme from sphinx-rtd-theme to Furo

## Context

### Background

The inewave documentation currently uses `sphinx-rtd-theme` (Read the Docs theme), which has limited mobile support, no dark mode, and a dated visual appearance. Furo is a modern, actively maintained Sphinx theme that provides responsive design, dark/light mode toggle, better typography, and cleaner navigation. It is the de facto standard for modern Python project documentation.

### Relation to Epic

This is the first ticket in Epic 2 (Sphinx Modernization). The theme migration must complete before any new documentation content is written (Epic 3) to ensure all content is authored and tested against the Furo theme.

### Current State

The Sphinx configuration at `/home/rogerio/git/inewave/docs/source/conf.py`:

- `html_theme = "sphinx_rtd_theme"` on line 89
- `html_theme_options` contains RTD-specific options: `logo_only`, `collapse_navigation`, `sticky_navigation`, `navigation_depth`, `includehidden`, `titles_only`
- Extensions list includes `"sphinx_rtd_theme"` on line 51
- `pygments_style = "sphinx"` on line 81
- Custom logo at `_static/logo_inewave_svg.svg`
- `html_static_path = ["_static/"]`
- Language set to `pt_BR`

The `pyproject.toml` lists `sphinx-rtd-theme` in the docs dependency group.

## Specification

### Requirements

1. Replace `sphinx-rtd-theme` with `furo` in `pyproject.toml` docs dependencies
2. Update `docs/source/conf.py`:
   - Change `html_theme` from `"sphinx_rtd_theme"` to `"furo"`
   - Remove `"sphinx_rtd_theme"` from the `extensions` list (Furo does not need to be listed as an extension)
   - Replace `html_theme_options` with Furo-compatible options (sidebar navigation, light/dark toggle)
   - Keep the custom logo (`html_logo`)
   - Update `pygments_style` to work well with both light and dark modes (use `"default"` or remove the line to let Furo handle it)
   - Add `pygments_dark_style` for dark mode syntax highlighting (e.g., `"monokai"`)
3. Verify all existing RST files render correctly with Furo
4. Verify sphinx-build completes without errors or warnings

### Inputs/Props

- File: `/home/rogerio/git/inewave/docs/source/conf.py`
- File: `/home/rogerio/git/inewave/pyproject.toml`
- Directory: `/home/rogerio/git/inewave/docs/source/` (all RST files)

### Outputs/Behavior

- Documentation builds with Furo theme
- Dark mode toggle is functional
- Custom logo displays correctly
- All existing pages (apresentacao, geral, referencia) render without layout issues

### Error Handling

- If any RST directive is RTD-theme-specific and breaks with Furo, it must be replaced with a Furo-compatible equivalent or standard Sphinx directive.

## Acceptance Criteria

- [ ] Given the updated `conf.py`, when reading the `html_theme` variable, then its value is `"furo"`
- [ ] Given the updated `conf.py`, when searching for `sphinx_rtd_theme` in the extensions list, then no match is found
- [ ] Given the updated `pyproject.toml`, when reading the `docs` dependency group, then `furo` is present and `sphinx-rtd-theme` is absent
- [ ] Given the updated documentation source, when running `uv run sphinx-build -M html docs/source docs/build`, then the command exits with code 0 and produces no errors
- [ ] Given the built documentation at `docs/build/html/index.html`, when opening it in a browser, then the Furo theme is visible with a dark mode toggle in the navigation bar

## Implementation Guide

### Suggested Approach

1. Update `/home/rogerio/git/inewave/pyproject.toml`:
   - In the `docs` dependency group, replace `"sphinx-rtd-theme"` with `"furo"`
2. Update `/home/rogerio/git/inewave/docs/source/conf.py`:
   - Remove `"sphinx_rtd_theme"` from the `extensions` list (line 51)
   - Change `html_theme = "sphinx_rtd_theme"` to `html_theme = "furo"` (line 89)
   - Replace `html_theme_options` with:
     ```python
     html_theme_options = {
         "sidebar_hide_name": True,
         "navigation_with_keys": True,
     }
     ```
   - Remove `pygments_style = "sphinx"` (let Furo use its default) or set to `"friendly"`
   - Add `pygments_dark_style = "monokai"` for dark mode
   - Keep `html_logo`, `html_static_path`, and all other non-theme settings unchanged
3. Run `uv sync --extra docs` to install Furo
4. Run `uv run sphinx-build -M html docs/source docs/build` to verify the build
5. Open `docs/build/html/index.html` in a browser and verify:
   - Logo displays correctly
   - Navigation works (sidebar, toctree)
   - Dark mode toggle functions
   - All existing pages render without broken layouts
   - Code blocks have syntax highlighting in both modes

### Key Files to Modify

- `/home/rogerio/git/inewave/docs/source/conf.py`
- `/home/rogerio/git/inewave/pyproject.toml`

### Patterns to Follow

- Furo does not need to be in the extensions list (unlike sphinx-rtd-theme which did)
- Use `sidebar_hide_name: True` when a logo is present to avoid redundant text
- Let Furo manage `pygments_style` defaults for light mode; only customize `pygments_dark_style` for dark mode

### Pitfalls to Avoid

- Do NOT keep `"sphinx_rtd_theme"` in the extensions list. Furo will conflict with it if both are present.
- Do NOT use RTD-specific theme options with Furo. The options `logo_only`, `collapse_navigation`, `sticky_navigation`, `navigation_depth`, `includehidden`, `titles_only` are RTD-specific and will be ignored or cause warnings with Furo.
- The `default_role = "obj"` setting in conf.py is not theme-related and should be kept.
- The `numpydoc_show_class_members = False` setting is not theme-related and should be kept.
- Check that the SVG logo (`logo_inewave_svg.svg`) renders properly in Furo's sidebar. SVG logos may need different sizing compared to RTD theme.

## Testing Requirements

### Unit Tests

- Not applicable (documentation configuration change)

### Integration Tests

- Run `uv run sphinx-build -M html docs/source docs/build` and verify exit code 0
- Run `uv run sphinx-build -M html docs/source docs/build -W` (warnings as errors) to catch any warnings
- Visually inspect `docs/build/html/index.html` and at least 3 other pages (a reference page, an example page, the tutorial)

### E2E Tests

- Not applicable

## Dependencies

- **Blocked By**: ticket-003-migrate-docs-deployment.md (docs deployment pipeline should be updated first)
- **Blocks**: ticket-007-update-sphinx-gallery-examples.md, all Epic 3 tickets

## Effort Estimate

**Points**: 3
**Confidence**: High
