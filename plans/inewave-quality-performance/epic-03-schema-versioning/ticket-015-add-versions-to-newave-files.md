# ticket-015 Add VERSIONS dictionaries to newave SectionFile classes

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Based on the version catalog produced in ticket-014, add `VERSIONS` dictionaries to all newave SectionFile/RegisterFile classes that have version-dependent formats. This enables `read(version=...)` for version-aware file reading of NEWAVE input files like dger.dat, confhd.dat, patamar.dat, etc.

## Anticipated Scope

- **Files likely to be modified**: `inewave/newave/dger.py`, `inewave/newave/confhd.py`, `inewave/newave/patamar.py`, and other version-sensitive newave handlers (exact list from ticket-014 catalog)
- **Key decisions needed**: Which section block classes need version variants; whether to create new block classes for each version or use conditional logic
- **Open questions**:
  - How many newave files actually vary between versions? The catalog from ticket-014 will answer this.
  - For SectionFile classes with many sections (e.g., Dger with 90+ sections), do only some sections change between versions, or does the entire section list change?
  - Should version-specific section classes live in the same model file or in separate files?

## Dependencies

- **Blocked By**: ticket-014
- **Blocks**: ticket-017, ticket-018

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
