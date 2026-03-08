# ticket-009 Create FAQ Documentation Page

## Context

### Background

Users of inewave frequently encounter the same set of questions about installation, compatibility with NEWAVE versions, common usage patterns, and error troubleshooting. Currently there is no FAQ page, so these questions are answered ad-hoc in GitHub issues. A dedicated FAQ page in the documentation will reduce repetitive support requests and help users self-serve.

### Relation to Epic

This is the second content-expansion ticket in Epic 3. It creates a new FAQ page organized by category. The page will be referenced from the updated toctree in ticket-012.

### Current State

- No FAQ page exists in the documentation.
- The existing docs have: `apresentacao.rst` (brief overview), `instalacao.rst` (installation), `tutorial.rst` (usage tutorial), `contribuicao.rst` (contributing).
- Common user pain points visible from the codebase:
  - cfinterface version compatibility (`cfinterface>=1.9.0` in pyproject.toml, but cfinterface<=1.8.3 pin was needed in earlier versions due to breaking changes).
  - Python version requirement is `>= 3.10` (pyproject.toml).
  - The library uses `read()` class method and `write()` instance method patterns.
  - Output files (nwlistop, nwlistcf) are read-only (no `write()` support).
  - DataFrame property access patterns (`.vazoes`, `.valores`, etc.).
  - The `VERSIONS` dict pattern in some file classes for handling different NEWAVE versions.
- All documentation is in Brazilian Portuguese.
- Furo theme is active.

## Specification

### Requirements

1. Create a new file `docs/source/geral/faq.rst` containing at least 15 questions and answers, entirely in Brazilian Portuguese.
2. Organize the FAQ into these categories using RST section headings:
   - **Instalacao** (3+ questions): pip install, version pinning, Python version compatibility, uv usage.
   - **Uso Geral** (4+ questions): read/write pattern, DataFrame output, output file limitations, file encoding.
   - **Compatibilidade com Versoes do NEWAVE** (3+ questions): how the library handles different NEWAVE output versions, the `VERSIONS` dict, cfinterface version requirements.
   - **Resolucao de Problemas** (3+ questions): import errors, cfinterface conflicts, file parsing failures, encoding issues.
   - **Desempenho** (2+ questions): slow imports, large file processing, link to performance guide (ticket-010).
3. Each Q&A should use a consistent RST format: the question as a bold paragraph or rubric, followed by the answer text.
4. Include `.. code-block:: python` examples where answers involve code.
5. Use `.. seealso::` to cross-reference other documentation pages (tutorial, installation, architecture).
6. Do NOT modify `docs/source/index.rst` — that is handled by ticket-012.
7. Do NOT modify any other existing documentation files.

### Inputs/Props

- Existing installation docs at `docs/source/geral/instalacao.rst` for reference.
- Tutorial at `docs/source/geral/tutorial.rst` for usage pattern reference.
- `pyproject.toml` for version requirements and dependency info.

### Outputs/Behavior

- A single new file `docs/source/geral/faq.rst` that renders correctly with `sphinx-build`.
- The page uses the RST label `.. _faq:` at the top for cross-referencing.
- All text content is in Brazilian Portuguese.

### Error Handling

- Not applicable — this is static content.

## Acceptance Criteria

- [ ] Given the file `docs/source/geral/faq.rst` exists, when counting the question entries (bold or rubric-formatted lines starting with a question), then there are at least 15 distinct questions
- [ ] Given the file `docs/source/geral/faq.rst` exists, when inspecting its structure, then it contains section headings for all 5 required categories (Instalacao, Uso Geral, Compatibilidade com Versoes do NEWAVE, Resolucao de Problemas, Desempenho)
- [ ] Given the file `docs/source/geral/faq.rst` exists, when inspecting its content, then all prose text is in Brazilian Portuguese
- [ ] Given the file `docs/source/geral/faq.rst` exists, when inspecting its content, then it contains at least 2 `.. code-block:: python` directives with usage examples
- [ ] Given the file `docs/source/geral/faq.rst` exists, when inspecting its content, then the RST label `.. _faq:` appears on line 1

## Implementation Guide

### Suggested Approach

1. Create `docs/source/geral/faq.rst`.
2. Start with `.. _faq:` label and heading "Perguntas Frequentes (FAQ)".
3. Add a brief introductory paragraph explaining what this page covers.
4. Write each category as an RST section (using `-` underline for category headings).
5. For each question, use the RST `.. rubric::` directive or bold text (`**Pergunta?**`) followed by answer paragraphs.
6. Suggested questions (minimum — add more as needed):
   - **Instalacao**: How to install, how to install specific version, Python version compatibility, using uv.
   - **Uso Geral**: How to read a file, how to write a file, why output files have no write(), how to get DataFrame output, how to handle files not in default encoding.
   - **Compatibilidade**: What NEWAVE versions are supported, how VERSIONS dict works, cfinterface version requirements.
   - **Resolucao de Problemas**: ImportError for cfinterface, UnicodeDecodeError on file read, KeyError when accessing properties, file not found patterns.
   - **Desempenho**: Why first import is slow (lazy imports), how to optimize reading many files.

### Key Files to Modify

- `docs/source/geral/faq.rst` (new file)

### Patterns to Follow

- Use the same RST heading hierarchy as other pages in `docs/source/geral/`: `=` for page title, `-` for sections.
- Use `.. code-block:: python` for code examples (same as `tutorial.rst`).
- Use `:ref:` for internal cross-references to other doc pages.

### Pitfalls to Avoid

- Do NOT add the FAQ to `index.rst` — that is ticket-012's job.
- Do NOT translate Python code, class names, or error messages to Portuguese — only prose.
- Do NOT reference specific GitHub issue numbers (they may become stale).
- Do NOT include questions about features that do not exist in the library.

## Testing Requirements

### Unit Tests

Not applicable — documentation-only ticket.

### Integration Tests

- Run `sphinx-build -b html docs/source docs/build` and verify no new errors are introduced. The file will not appear in navigation until ticket-012 adds it to the toctree.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-006-migrate-sphinx-theme.md
- **Blocks**: ticket-012-update-index-toctree.md

## Effort Estimate

**Points**: 3
**Confidence**: High
