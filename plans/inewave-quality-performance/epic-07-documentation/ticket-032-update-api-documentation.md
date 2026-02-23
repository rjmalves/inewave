# ticket-032 Update API documentation and docstrings

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Update all sphinx docstrings and API reference documentation to reflect the changes made in epics 01-05. This includes: new base classes (TabelaSerieAnual, TabelaSeriePatamarAnual), updated archive base classes, version-aware read API, and validation API. Ensure the sphinx build produces clean HTML documentation.

## Anticipated Scope

- **Files likely to be modified**: All production files modified in earlier epics (docstring updates), `docs/source/` RST files (API reference), `docs/source/conf.py` (if sphinx configuration changes needed)
- **Key decisions needed**: Docstring format (numpydoc vs. Google style -- existing code uses numpydoc/RST); whether to auto-generate API docs with sphinx-apidoc
- **Open questions**:
  - Are the existing docs up-to-date with the pre-migration codebase?
  - Do the new base classes need dedicated documentation pages?
  - Should the docs include architecture diagrams showing the new class hierarchy?

## Dependencies

- **Blocked By**: ticket-013
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
