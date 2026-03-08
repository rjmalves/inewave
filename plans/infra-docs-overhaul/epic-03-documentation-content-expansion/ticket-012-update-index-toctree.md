# ticket-012 Update index.rst Toctree for New Pages

## Context

### Background

Tickets 008, 009, 010, and 011 create new documentation pages and improve existing ones, but none of them modify `docs/source/index.rst`. This final integration ticket updates the main toctree to incorporate all new pages into the site navigation, ensuring users can discover and navigate to the new content.

### Relation to Epic

This is the final ticket in Epic 3, integrating all new content pages into the documentation site's navigation structure. It depends on all other tickets in this epic being completed first.

### Current State

The current `docs/source/index.rst` has this toctree structure:

```rst
.. toctree::
   :caption: Apresentacao
   :maxdepth: 3

   apresentacao/apresentacao.rst

.. toctree::
   :caption: Geral
   :maxdepth: 3

   geral/instalacao
   geral/tutorial
   examples/index.rst
   geral/contribuicao

.. toctree::
   :caption: Referencia
   :maxdepth: 2

   referencia/newave/index.rst
   referencia/nwlistcf/index.rst
   referencia/nwlistop/index.rst
   referencia/libs/index.rst
```

New pages created by this epic:

- `docs/source/geral/arquitetura.rst` (ticket-008)
- `docs/source/geral/faq.rst` (ticket-009)
- `docs/source/geral/desempenho.rst` (ticket-010)

Note: ticket-011 modifies existing reference index pages but does not create new pages needing toctree entries.

## Specification

### Requirements

1. Modify `docs/source/index.rst` to add the 3 new pages to the toctree.
2. Create a new toctree section with caption "Guias" (between the "Geral" and "Referencia" sections) containing:
   - `geral/arquitetura`
   - `geral/desempenho`
   - `geral/faq`
3. Keep the existing "Apresentacao", "Geral", and "Referencia" toctree sections unchanged — do NOT reorder or remove any existing entries.
4. The "Guias" section should use `:maxdepth: 2`.
5. All caption text must be in Brazilian Portuguese (they already are, and "Guias" is Portuguese).
6. Ensure the accented characters in existing captions ("Apresentacao", "Referencia") are preserved exactly as they currently appear in the file.

### Inputs/Props

- The current `docs/source/index.rst` content (shown in Current State above).
- The file paths of the 3 new pages created by tickets 008-010.

### Outputs/Behavior

- `docs/source/index.rst` is updated with a new "Guias" toctree section.
- The Furo sidebar navigation shows the new "Guias" section with links to Architecture, Performance, and FAQ pages.
- All existing navigation entries continue to work.

### Error Handling

- If any of the 3 new RST files do not exist when `sphinx-build` runs, Sphinx will emit an error about missing toctree entries. This ticket assumes all 3 files are already created by tickets 008-010.

## Acceptance Criteria

- [ ] Given the file `docs/source/index.rst`, when inspecting its toctree directives, then there are exactly 4 toctree blocks with captions "Apresentacao", "Geral", "Guias", and "Referencia" in that order
- [ ] Given the file `docs/source/index.rst`, when inspecting the "Guias" toctree block, then it contains entries for `geral/arquitetura`, `geral/desempenho`, and `geral/faq`
- [ ] Given the file `docs/source/index.rst`, when inspecting the "Geral" toctree block, then it contains the original 4 entries (`geral/instalacao`, `geral/tutorial`, `examples/index.rst`, `geral/contribuicao`) in the original order
- [ ] Given the file `docs/source/index.rst`, when inspecting the "Referencia" toctree block, then it contains the original 4 entries in the original order
- [ ] Given all new pages exist and `sphinx-build -b html docs/source docs/build` is run, then the build completes without toctree-related errors

## Implementation Guide

### Suggested Approach

1. Open `docs/source/index.rst`.
2. After the "Geral" toctree block and before the "Referencia" toctree block, insert:

   ```rst
   .. toctree::
      :caption: Guias
      :maxdepth: 2

      geral/arquitetura
      geral/desempenho
      geral/faq
   ```

3. Do not modify any other toctree block.
4. Verify by running `sphinx-build -b html docs/source docs/build`.

### Key Files to Modify

- `docs/source/index.rst`

### Patterns to Follow

- Follow the exact same toctree format used by the existing blocks: `.. toctree::` directive, `:caption:` option, `:maxdepth:` option, blank line, indented file paths without `.rst` extension (matching existing convention where some entries omit the extension).

### Pitfalls to Avoid

- Do NOT use `.rst` extension for the new entries — follow the convention of the "Geral" section which omits extensions for entries like `geral/instalacao`.
- Do NOT reorder existing entries in any toctree block.
- Do NOT change existing captions or maxdepth values.
- Do NOT add ticket-011's reference pages to a toctree — they are already in the "Referencia" section via their existing module index files.

## Testing Requirements

### Unit Tests

Not applicable — documentation-only ticket.

### Integration Tests

- Run `sphinx-build -b html docs/source docs/build` and verify:
  1. The build completes without errors related to missing toctree entries.
  2. The generated HTML sidebar shows the "Guias" section with 3 entries.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-008-create-architecture-page.md, ticket-009-create-faq-page.md, ticket-010-create-performance-guide.md, ticket-011-improve-api-reference.md
- **Blocks**: None

## Effort Estimate

**Points**: 1
**Confidence**: High
