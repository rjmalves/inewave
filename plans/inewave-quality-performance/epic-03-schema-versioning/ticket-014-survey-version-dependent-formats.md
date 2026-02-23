# ticket-014 Survey and catalog version-dependent file formats

## Context

### Background

The inewave library parses output files from the NEWAVE hydrothermal dispatch model. Different NEWAVE releases (v27, v28, v28.12, v28.16, v29.2, v29.4.1, v30, etc.) produce output files with different column widths, field formats, and section structures. The cfinterface framework supports this via the `VERSIONS` dictionary pattern on `BlockFile`, `SectionFile`, and `RegisterFile` classes. Currently, only 5 inewave file handlers declare `VERSIONS`:

1. `inewave/nwlistop/cmarg.py` -- versions `"27"` and `"29.4.1"` (patamar float field width 8 vs 11)
2. `inewave/nwlistop/cmargmed.py` -- versions `"28"` and `"29.4.1"` (float field width 8/10-stride vs 11/11-stride)
3. `inewave/nwlistop/pivarm.py` -- versions `"28.12"` and `"29.2"` (FloatField decimal vs `format="E"`)
4. `inewave/nwlistop/pivarmincr.py` -- versions `"28.12"` and `"29.2"` (same pattern as pivarm)
5. `inewave/newave/avl_cortesfpha_nwv.py` -- versions `"28"` and `"28.16"` (different version header block + table block)

This ticket produces a comprehensive catalog of all files that need `VERSIONS` dictionaries, directly informing the implementation work in tickets 015 and 016.

### Relation to Epic

This is the research/documentation foundation for Epic 03. All subsequent tickets (015-018) depend on the catalog produced here to know which files to modify, what version keys to use, and what format changes to express.

### Current State

After Epic 02, all nwlistop model files have been migrated to `TabelaSerieAnual` / `TabelaSeriePatamarAnual` base classes with `COLUMNS` definitions. Version differences in nwlistop files are expressed as different `FloatField` sizes or `format="E"` parameters in COLUMNS. The 5 existing VERSIONS files demonstrate the pattern. The newave module has SectionFile classes (e.g., `Dger`, `Patamar`, `Sistema`, `Confhd`) and BlockFile classes (e.g., `Pmo`, `Parp`, `Cvar`) -- none of which currently declare VERSIONS.

## Specification

### Requirements

1. **Audit all handler files** in `inewave/nwlistop/` (approx. 120+ `.py` files, excluding `__init__.py`) and `inewave/newave/` (approx. 75+ `.py` files) to identify which ones have format differences across NEWAVE versions.
2. **Analyze the existing 5 VERSIONS files** to understand the version key naming convention already in use (numeric strings like `"27"`, `"28"`, `"28.12"`, `"28.16"`, `"29.2"`, `"29.4.1"`).
3. **Check git history** of model files for format-changing commits (search for commits that changed `FloatField` sizes, added new block/section classes, or modified column layouts).
4. **Produce a catalog file** at `plans/inewave-quality-performance/version-catalog.md` documenting:
   - Every file handler that has known format differences between NEWAVE versions
   - The version keys to use (following the existing lexicographic string convention)
   - What specifically changes between versions (field widths, field formats, section lists, block types)
   - The model file(s) affected and whether new model classes are needed or existing ones suffice
   - Classification: `nwlistop-BlockFile`, `newave-SectionFile`, `newave-BlockFile`, or `newave-RegisterFile`

### Inputs/Props

- Source files: all `inewave/nwlistop/*.py` and `inewave/newave/*.py` handler files
- Source files: all `inewave/nwlistop/modelos/*.py` and `inewave/newave/modelos/*.py` model files
- Git history of the inewave repository
- The 5 existing VERSIONS declarations as reference patterns

### Outputs/Behavior

A single markdown catalog file at `plans/inewave-quality-performance/version-catalog.md` with the following structure:

```markdown
# Version-Dependent File Catalog

## Version Key Convention

[Document the lexicographic string convention and which NEWAVE versions are represented]

## Already Versioned (5 files)

[Table listing each file, its version keys, and what changes]

## Needs VERSIONS -- nwlistop BlockFile (N files)

[Table: handler file | model file | base archive class | version keys | what changes]

## Needs VERSIONS -- newave SectionFile (N files)

[Table: handler file | section classes affected | version keys | what changes]

## Needs VERSIONS -- newave BlockFile (N files)

[Table: handler file | block classes affected | version keys | what changes]

## No Versioning Needed

[List of files confirmed to have no version-dependent format changes, with brief justification]

## Open Questions / Unknowns

[Any format changes that could not be confirmed from code or git history alone]
```

### Error Handling

- If a file's format history cannot be determined from code or git history, list it under "Open Questions / Unknowns" rather than omitting it.
- If a version difference is suspected but not confirmed, document it as "suspected" with the evidence found.

## Acceptance Criteria

- [ ] Given the catalog file exists at `plans/inewave-quality-performance/version-catalog.md`, when opened, then it contains entries for all 5 already-versioned files with accurate version keys matching the source code.
- [ ] Given the catalog, when comparing its "Needs VERSIONS" lists against the actual handler files, then every handler file in `inewave/nwlistop/` and `inewave/newave/` is accounted for (either in a "Needs VERSIONS" section or in "No Versioning Needed").
- [ ] Given the catalog, when reading the version key convention section, then it explains the lexicographic string comparison used by `cfinterface.versioning.resolve_version()` and documents the existing keys (`"27"`, `"28"`, `"28.12"`, `"28.16"`, `"29.2"`, `"29.4.1"`).
- [ ] Given the catalog, when reading any "Needs VERSIONS" entry, then it specifies: (a) the exact handler file path, (b) the exact model file path(s), (c) the version keys to declare, (d) what changes between versions (field widths, section lists, etc.), and (e) whether new model classes are needed.
- [ ] Given no code files are modified by this ticket, when running `pytest`, then the full test suite (1126+ tests) passes unchanged.

## Implementation Guide

### Suggested Approach

1. **Start with the existing 5 VERSIONS files** to establish the pattern:
   - Read `inewave/nwlistop/cmarg.py`, `cmargmed.py`, `pivarm.py`, `pivarmincr.py`, `inewave/newave/avl_cortesfpha_nwv.py`
   - Note their version keys, the block/section class variants, and what differs between variants
2. **Scan all nwlistop model files** (`inewave/nwlistop/modelos/*.py`) for files that define multiple block classes with different field sizes or formats (e.g., a `FooAnos` and `FooAnos27` class in the same file). After Epic 02, these are `TabelaSerieAnual` / `TabelaSeriePatamarAnual` subclasses with different `COLUMNS`.
3. **Scan all nwlistop handler files** (`inewave/nwlistop/*.py`) for those that import version-variant model classes. Check if they already have VERSIONS or if VERSIONS needs to be added.
4. **Scan newave handler files** (`inewave/newave/*.py`) for SectionFile/BlockFile/RegisterFile classes. Check git history for commits that changed SECTIONS/BLOCKS lists or section/block model classes.
5. **Search git log** for commits mentioning version changes, field width changes, or format updates: `git log --all --oneline --grep="versao" --grep="version" --grep="FloatField" --grep="format" -- inewave/`.
6. **Cross-reference with nwlistop model files** that have multiple class definitions (e.g., `cmarg.py` defines both `CmargsAnos27` and `CmargsAnos`). Any model file with 2+ classes likely corresponds to version differences.
7. **Write the catalog** following the structure in the Outputs section above.

### Key Files to Inspect

- All handler files: `inewave/nwlistop/*.py` (120+ files) and `inewave/newave/*.py` (75+ files)
- All model files: `inewave/nwlistop/modelos/*.py` and `inewave/newave/modelos/*.py`
- Existing VERSIONS examples: `inewave/nwlistop/cmarg.py`, `inewave/nwlistop/cmargmed.py`, `inewave/nwlistop/pivarm.py`, `inewave/nwlistop/pivarmincr.py`, `inewave/newave/avl_cortesfpha_nwv.py`
- cfinterface versioning API: `/home/rogerio/git/cfinterface/cfinterface/versioning.py` (for `resolve_version()` lexicographic comparison semantics)

### Patterns to Follow

- Version keys are **lexicographic strings** compared by `resolve_version()`. The function returns the component list for the most recent version key `<=` the requested key. Keys like `"28.12"` are compared as strings, not semver.
- Existing convention uses bare numeric strings: `"27"`, `"28"`, `"28.12"`, `"28.16"`, `"29.2"`, `"29.4.1"`.
- `BLOCKS` / `SECTIONS` is the "latest" / default component list. `VERSIONS` maps older version keys to their specific component lists.

### Pitfalls to Avoid

- **Do not modify any source code** -- this is a research ticket only.
- **Do not assume version differences from class naming alone** -- verify by inspecting COLUMNS definitions or section implementations.
- The `resolve_version()` comparison is lexicographic, not semantic. `"28.12"` < `"28.16"` < `"28.2"` lexicographically (because `"28.12"` < `"28.16"` < `"28.2"`). The existing codebase is aware of this and uses keys accordingly. Do not "fix" this.
- Some model files define multiple classes for historical reasons (different data sources) rather than NEWAVE version differences. Do not confuse these.

## Testing Requirements

### Unit Tests

No code is modified. No new tests needed.

### Integration Tests

Not applicable.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-013 (completed -- Epic 02 cleanup)
- **Blocks**: ticket-015, ticket-016

## Effort Estimate

**Points**: 2
**Confidence**: High
