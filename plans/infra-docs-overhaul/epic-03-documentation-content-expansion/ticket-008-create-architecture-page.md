# ticket-008 Create Architecture Documentation Page

## Context

### Background

The inewave library has a rich internal architecture based on the cfinterface framework, but the only documentation of this architecture lives in the contribution page (`docs/source/geral/contribuicao.rst`). That page mixes framework description with development guidelines, making it hard for users and new contributors to understand the library's design in isolation. A dedicated architecture page will provide a clear, self-contained explanation of the library's structure, file classification model, and module organization.

### Relation to Epic

This is the first content-expansion ticket in Epic 3. It creates a new standalone RST page explaining the library's internal design. The architecture page will be referenced from the updated toctree in ticket-012.

### Current State

- The contribution page at `docs/source/geral/contribuicao.rst` contains a section titled "O framework cfinterface e dependencias de desenvolvimento" that describes the three file classification models (BlockFile, SectionFile, RegisterFile) with cross-references to cfinterface classes.
- The library has four top-level modules: `inewave.newave`, `inewave.nwlistop`, `inewave.nwlistcf`, `inewave.libs`, plus internal `inewave._utils` and `inewave.config`.
- Each subpackage uses a lazy import mechanism via `_LAZY_IMPORTS` dict in its `__init__.py`, mapping class names to module filenames.
- Sphinx conf.py has `intersphinx_mapping` configured for cfinterface at `https://rjmalves.github.io/cfinterface/`.
- The Furo theme is already active (`html_theme = "furo"` in `docs/source/conf.py`).
- All documentation is in Brazilian Portuguese.

## Specification

### Requirements

1. Create a new file `docs/source/geral/arquitetura.rst` containing the architecture documentation page, entirely in Brazilian Portuguese.
2. The page must cover these topics in order:
   - **Visao Geral**: Brief overview of inewave as a file I/O library for the NEWAVE model.
   - **Framework cfinterface**: Explanation of the three file classification models (BlockFile, SectionFile, RegisterFile) with intersphinx cross-references to cfinterface classes. This content should be rewritten and expanded from the existing contribution page, not copy-pasted.
   - **Estrutura de Modulos**: Description of the four public modules (`newave`, `nwlistop`, `nwlistcf`, `libs`) and what each contains (input files, output files, shared utilities).
   - **Mecanismo de Lazy Import**: How the `_LAZY_IMPORTS` dict and `__getattr__` pattern work in each subpackage's `__init__.py` to defer module loading.
   - **Convencoes de Nomenclatura**: How NEWAVE file names map to Python class names (PascalCase), and how properties use snake_case with DataFrame outputs.
   - **Fluxo de Dados**: How a typical `read()` / `write()` cycle works end-to-end: file on disk -> cfinterface parsing -> Block/Section/Register components -> Python class properties -> pandas DataFrames.
3. Use RST admonitions (`.. note::`, `.. seealso::`) where appropriate.
4. Include at least one `.. code-block:: python` example showing a simple read operation.
5. Use intersphinx references (`:obj:`) to link to cfinterface classes (BlockFile, SectionFile, RegisterFile, Block, Section, Register).
6. Do NOT include UML diagrams or images — keep it text-only RST.
7. Do NOT modify `docs/source/geral/contribuicao.rst` — the architecture page is additive, not a replacement.
8. Do NOT modify `docs/source/index.rst` — that is handled by ticket-012.

### Inputs/Props

- Existing content in `docs/source/geral/contribuicao.rst` (lines 1-37) as reference material for the cfinterface framework description.
- Module structure visible in `inewave/newave/__init__.py` (lazy import pattern), `inewave/config.py` (constants), `inewave/_utils/` (internal utilities).

### Outputs/Behavior

- A single new file `docs/source/geral/arquitetura.rst` that renders correctly with `sphinx-build`.
- The page uses the RST label `.. _arquitetura:` at the top for cross-referencing.
- All text content is in Brazilian Portuguese.

### Error Handling

- If intersphinx links to cfinterface fail to resolve (due to cfinterface docs being unavailable), the build should still succeed with unresolved reference warnings. Do not add `nitpicky = True` to conf.py.

## Acceptance Criteria

- [ ] Given the file `docs/source/geral/arquitetura.rst` exists, when inspecting its content, then it contains the RST label `.. _arquitetura:` on line 1
- [ ] Given the file `docs/source/geral/arquitetura.rst` exists, when inspecting its content, then it contains sections for all 6 required topics (Visao Geral, Framework cfinterface, Estrutura de Modulos, Mecanismo de Lazy Import, Convencoes de Nomenclatura, Fluxo de Dados)
- [ ] Given the file `docs/source/geral/arquitetura.rst` exists, when inspecting its content, then all prose text is in Brazilian Portuguese
- [ ] Given the file `docs/source/geral/arquitetura.rst` exists, when inspecting its content, then it contains at least one `.. code-block:: python` directive with a read example
- [ ] Given the file `docs/source/geral/arquitetura.rst` exists, when inspecting its content, then it contains `:obj:` cross-references to at least `BlockFile`, `SectionFile`, and `RegisterFile`

## Implementation Guide

### Suggested Approach

1. Create `docs/source/geral/arquitetura.rst`.
2. Start with the `.. _arquitetura:` label and a top-level heading "Arquitetura do inewave".
3. Write each section in order. For the cfinterface section, use the content from `contribuicao.rst` lines 1-37 as reference but rewrite it to be more explanatory and less contributor-focused.
4. For the lazy import section, reference the `_LAZY_IMPORTS` pattern visible in `inewave/newave/__init__.py`.
5. For the data flow section, describe the lifecycle of a `read()` call: disk -> `open()` -> cfinterface file class dispatches to Block/Section/Register components -> components parse raw text/binary -> Python properties return pandas DataFrames.
6. Validate the RST syntax by checking that the file can be parsed without errors (run `python -m rst2html docs/source/geral/arquitetura.rst /dev/null` or equivalent).

### Key Files to Modify

- `docs/source/geral/arquitetura.rst` (new file)

### Patterns to Follow

- Follow the RST heading style used in existing docs: `=` for title, `-` for section, `~` for subsection (see `contribuicao.rst` for reference).
- Use `.. code-block:: python` for code examples (same pattern as `tutorial.rst`).
- Use `:obj:` for intersphinx cross-references (same pattern as `contribuicao.rst`).

### Pitfalls to Avoid

- Do NOT translate Python keywords, class names, or module names to Portuguese — only prose text is in Portuguese.
- Do NOT copy-paste content verbatim from `contribuicao.rst` — rewrite it with an architecture focus rather than a contributor focus.
- Do NOT add this page to `index.rst` — that is ticket-012's responsibility.
- Do NOT include diagrams or images that require additional Sphinx extensions.

## Testing Requirements

### Unit Tests

Not applicable — this is a documentation-only ticket.

### Integration Tests

- Run `sphinx-build -W -b html docs/source docs/build` (or `sphinx-build -b html docs/source docs/build` if `-W` fails due to pre-existing warnings from cfinterface/gallery) and verify no new errors are introduced by the new file. Note: the file will NOT appear in navigation until ticket-012 adds it to the toctree, but sphinx-build should still parse it without errors.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-006-migrate-sphinx-theme.md, ticket-007-update-sphinx-gallery-examples.md
- **Blocks**: ticket-012-update-index-toctree.md

## Effort Estimate

**Points**: 3
**Confidence**: High
