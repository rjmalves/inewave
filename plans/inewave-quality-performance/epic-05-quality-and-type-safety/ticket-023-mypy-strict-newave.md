# ticket-023 Enable mypy strict mode and fix newave module errors

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Enable mypy strict mode (`--strict`) for the `inewave/newave/` module and fix all resulting type errors. The newave module has ~150 files (76 handlers + 74 models) and is the most important module for type safety since it handles NEWAVE input files that downstream code depends on.

## Anticipated Scope

- **Files likely to be modified**: `pyproject.toml` or `mypy.ini` (mypy configuration), all files in `inewave/newave/` that produce strict-mode errors
- **Key decisions needed**: Whether to enable strict mode project-wide or per-module; whether to use `--strict` flag or individual strict options incrementally
- **Open questions**:
  - How many mypy strict errors currently exist in the newave module?
  - Are the errors primarily missing return types, untyped arguments, or more complex generics issues?
  - Does the cfinterface API have complete type stubs, or will inewave need `# type: ignore` for cfinterface calls?

## Dependencies

- **Blocked By**: ticket-013
- **Blocks**: ticket-024

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
