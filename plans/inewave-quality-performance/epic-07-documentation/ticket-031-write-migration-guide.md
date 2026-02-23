# ticket-031 Write migration guide for downstream users

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Create a comprehensive migration guide for downstream consumers (primarily sintetizador-newave) upgrading from inewave v1.12.x to v1.13+. The guide should document: dependency changes (cfinterface >= 1.9.0), new version-aware read API, deprecated classes (ValoresSerie, ValoresSeriePatamar), and any behavioral differences.

## Anticipated Scope

- **Files likely to be modified**: New file `docs/source/migration.rst` or `MIGRATION.md` at repo root
- **Key decisions needed**: Format (RST for sphinx integration vs. Markdown); level of detail for each change category
- **Open questions**:
  - What are the actual downstream consumers beyond sintetizador-newave?
  - Are there any breaking changes, or is everything backward compatible?
  - Should the guide include code examples showing old vs. new patterns?
  - Should deprecation timelines be specified (e.g., "ValoresSerie will be removed in v2.0")?

## Dependencies

- **Blocked By**: ticket-013 (need final state of codebase)
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
