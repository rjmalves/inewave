# ticket-016 Add VERSIONS dictionaries to nwlistop BlockFile classes

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Based on the version catalog (ticket-014), add `VERSIONS` dictionaries to nwlistop BlockFile classes that have version-dependent output formats. Currently 4 nwlistop files have VERSIONS (cmarg, cmargmed, pivarm, pivarmincr). This ticket expands coverage to all identified version-sensitive output files.

## Anticipated Scope

- **Files likely to be modified**: nwlistop handler files identified in the version catalog, plus their model files (new version-variant block classes using TabelaSerieAnual/TabelaSeriePatamarAnual)
- **Key decisions needed**: Whether version variants require new model classes or can be handled via field size adjustments on existing COLUMNS definitions
- **Open questions**:
  - After the TabularSection migration (Epic 02), will it be easier to express version differences as COLUMNS variations?
  - How many nwlistop output files actually vary between NEWAVE versions?
  - Can the existing VERSIONS pattern on cmarg/pivarm serve as a template?

## Dependencies

- **Blocked By**: ticket-014
- **Blocks**: ticket-017, ticket-018

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
