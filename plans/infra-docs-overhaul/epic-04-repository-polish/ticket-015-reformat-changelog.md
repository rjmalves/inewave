# ticket-015 Reformat CHANGELOG to Keep a Changelog Standard

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Reformat the existing CHANGELOG.md to follow the Keep a Changelog standard (https://keepachangelog.com/), adding proper version headers with dates, category grouping (Added, Changed, Deprecated, Fixed, Removed, Security), and comparison links between versions. The current CHANGELOG uses simple `# version` headings with flat bullet lists.

## Anticipated Scope

- **Files likely to be modified**: `/home/rogerio/git/inewave/CHANGELOG.md`
- **Key decisions needed**: Whether to include release dates (requires researching git tags or PyPI release dates); whether to add comparison links (`[1.13.0]: https://github.com/rjmalves/inewave/compare/v1.12.1...v1.13.0`); how to categorize existing entries that mix Added/Fixed/Changed
- **Open questions**: Are release dates available from git tags for all versions? Should entries be translated to fit KAC categories or kept as-is with just header reformatting? How far back should the reformatting go (all versions or just recent ones)?

## Dependencies

- **Blocked By**: None
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: Low (will be re-estimated during refinement)
