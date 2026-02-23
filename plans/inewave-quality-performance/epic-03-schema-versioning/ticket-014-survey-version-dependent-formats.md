# ticket-014 Survey and catalog version-dependent file formats

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Systematically survey all newave and nwlistop file handlers to identify which ones have format differences across NEWAVE versions (v27, v28, v29, v30, etc.). Produce a catalog documenting which files vary, what changes between versions, and which version keys to use in the VERSIONS dictionary. This catalog directly informs tickets 015-018.

## Anticipated Scope

- **Files likely to be modified**: None (this is a research/documentation ticket)
- **Output**: A catalog file at `plans/inewave-quality-performance/version-catalog.md`
- **Key decisions needed**: How to identify version-dependent formats (code analysis, documentation review, git history analysis of format-changing commits)
- **Open questions**:
  - Which NEWAVE versions are in active use by downstream consumers?
  - Are there format changes not visible in the codebase (i.e., formats that were never implemented but are known to exist)?
  - Should the version keys match NEWAVE release numbers exactly (e.g., "27", "29.4.1") or use a normalized format?
  - How do the existing 5 VERSIONS files (cmarg, cmargmed, pivarm, pivarmincr, avl_cortesfpha_nwv) define their version keys?

## Dependencies

- **Blocked By**: ticket-013
- **Blocks**: ticket-015, ticket-016

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
