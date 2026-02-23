# ticket-026 Clean up type ignore comments and add proper annotations

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Audit all `# type: ignore` comments across the inewave codebase, remove those that are no longer needed (especially after the TabularSection migration and mypy strict fixes), and replace remaining ones with specific ignore codes (e.g., `# type: ignore[assignment]` instead of bare `# type: ignore`). Also add proper type annotations to public functions and properties that are currently untyped.

## Anticipated Scope

- **Files likely to be modified**: Any file containing `# type: ignore` comments (spread across all modules)
- **Key decisions needed**: Which `# type: ignore` comments are still necessary after cfinterface v1.9.0 improvements; whether to use inline `# type: ignore[code]` or `pyright`-compatible ignore directives
- **Open questions**:
  - How many `# type: ignore` comments exist currently? What are the most common categories?
  - After mypy strict is enabled (tickets 023-024), how many remain?
  - Are there cfinterface API calls that legitimately require `# type: ignore` due to dynamic dispatch patterns?

## Dependencies

- **Blocked By**: ticket-024
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: Low (will be re-estimated during refinement)
