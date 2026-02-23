# ticket-026 Clean up type ignore comments and add proper annotations

## Context

### Background

After tickets 023-024 enable mypy strict mode and fix all type errors, and ticket-025 reduces duplication, the codebase will have mypy strict passing with 0 errors. However, 267 `# type: ignore` comments remain scattered across 156 files. Of these, 265 are bare `# type: ignore` (without specific error codes), and only 2 use specific codes (`# type: ignore[arg-type]`). Many of these comments are no longer needed or can be narrowed to specific error codes for better maintainability.

### Relation to Epic

This is the final ticket in Epic 05. It addresses goal #5: "Clean up `# type: ignore` comments where possible." It depends on tickets 023-024 being complete because the strict-mode configuration determines which `# type: ignore` comments are genuinely needed versus stale.

### Current State

There are **267 `# type: ignore` comments** across 156 files in the `inewave/` source directory. The breakdown is:

**Import-level comments (189 total):**

- 149 on `import pandas as pd  # type: ignore`
- 40 on `import numpy as np  # type: ignore`

These exist because at some point pandas and numpy lacked type stubs. Modern versions of both libraries ship with `py.typed` markers and inline type stubs. With pandas >= 2.2.3 and numpy >= 2.2.1 (the project's dependency floor), these `# type: ignore` comments are unnecessary and will be flagged as `unused-ignore` by mypy once strict mode is enabled.

**Non-import comments (76 total):**

- ~55 on `tabela = tabela[:i, :]  # type: ignore` (numpy array slicing). These appear in newave model files (`dger.py`, `pmo.py`, `parp.py`, `cvar.py`, `curva.py`, etc.) and in deprecated nwlistop block files. The ignore is needed because `tabela` is typed as `np.ndarray` (via `np.zeros(...)`) and the slice assignment `tabela[:i, :]` produces a type that mypy may not narrow correctly.
- ~13 on archive base files `import pandas as pd  # type: ignore` (already counted above but also affects archive files)
- 3 on `gtert.py` model (import and `DATA_LINE` construction with list concatenation)
- 2 with specific codes: `# type: ignore[arg-type]` in `TabelaSerieAnual` and `TabelaSeriePatamarAnual` (on `df["ano"] = int(self._ano)`)
- ~3 others: `forward.py` (DataFrame comparison), `pmo.py` (various), `sistema.py` (various)

After tickets 023-024, mypy will flag `unused-ignore` for any `# type: ignore` that suppresses no actual error. The exact set of truly-needed ignores will only be known after strict mode is active.

**Key files with multiple `# type: ignore` comments:**

- `inewave/newave/modelos/pmo.py` -- 19 comments
- `inewave/newave/modelos/parp.py` -- 11 comments
- `inewave/newave/modelos/parpvaz.py` -- 9 comments
- `inewave/newave/modelos/parpeol.py` -- 8 comments
- `inewave/newave/modelos/sistema.py` -- 7 comments
- `inewave/newave/modelos/patamar.py` -- 6 comments

## Specification

### Requirements

1. Run `mypy inewave/ --strict` after tickets 023-024 are complete to identify which `# type: ignore` comments are `unused-ignore`
2. Remove all `# type: ignore` comments flagged as `unused-ignore` by mypy
3. For remaining necessary `# type: ignore` comments, add specific error codes (e.g., `# type: ignore[assignment]`, `# type: ignore[arg-type]`, `# type: ignore[misc]`)
4. All 1134 existing tests must continue to pass
5. `mypy inewave/ --strict` must report 0 errors after cleanup
6. No behavioral changes

### Phase 1: Remove Stale Comments

After strict mode is enabled (tickets 023-024), run `mypy inewave/ --strict` and collect all `unused-ignore` warnings. Remove each flagged comment. Based on current analysis:

- **All 149 `import pandas as pd  # type: ignore`** will likely be flagged as unused (pandas >= 2.2.3 has stubs)
- **All 40 `import numpy as np  # type: ignore`** will likely be flagged as unused (numpy >= 2.2.1 has stubs)
- **Some non-import comments** may also be flagged if the strict mode annotations resolve the underlying type issue

Expected removal: ~200+ comments.

### Phase 2: Narrow Remaining Comments

For each remaining `# type: ignore` that is NOT flagged as unused:

1. Run `mypy` with `--show-error-codes` to identify the specific error code being suppressed
2. Replace `# type: ignore` with `# type: ignore[specific-code]`
3. Add a brief comment explaining WHY the ignore is needed, e.g.:
   ```python
   tabela = tabela[:i, :]  # type: ignore[index]  # numpy slice narrowing
   ```

Expected remaining comments: ~30-50 (mostly numpy array slicing patterns in newave models and the 2 existing `[arg-type]` in TabularSection base classes).

### Phase 3: Investigate Removable Ignores

For each remaining `# type: ignore` with specific code, assess whether the ignore can be eliminated by:

- Adding a `cast()` call
- Using `assert isinstance(...)` to narrow the type
- Refactoring the expression slightly

Do NOT remove an ignore if the alternative makes the code harder to read. The goal is to reduce noise, not introduce complexity.

### Inputs/Props

No new inputs.

### Outputs/Behavior

Zero behavioral changes. The only modifications are removal or narrowing of `# type: ignore` comments.

### Error Handling

No changes to error handling.

## Acceptance Criteria

- [ ] Given the inewave source, when searching for `# type: ignore$` (bare ignores without specific code), then 0 occurrences are found (all remaining ignores have specific error codes)
- [ ] Given `mypy inewave/ --strict`, when running it, then 0 errors are reported (including 0 `unused-ignore` warnings)
- [ ] Given the inewave source, when counting `# type: ignore` comments, then the total is reduced from 267 to fewer than 60
- [ ] Given any remaining `# type: ignore[code]` comment, when inspecting it, then it has a brief inline explanation of why the ignore is necessary
- [ ] Given the full test suite, when running `pytest`, then all 1134 tests pass
- [ ] Given the codebase, when running `ruff check inewave/`, then 0 errors are reported

## Implementation Guide

### Suggested Approach

1. **Ensure tickets 023-024 are complete.** Verify `mypy inewave/ --strict` reports 0 errors (this is a hard prerequisite).

2. **Run `mypy inewave/ --strict --warn-unused-ignores`** (should already be enabled in config). Collect all `unused-ignore` warnings into a list.

3. **Batch-remove import-level `# type: ignore` comments.** Use a regex search to find and remove:
   - `import pandas as pd  # type: ignore` -> `import pandas as pd`
   - `import numpy as np  # type: ignore` -> `import numpy as np`
     This covers 189 of the 267 comments.

4. **Remove non-import `unused-ignore` comments.** Process each one individually because some may need code adjustments.

5. **Run `mypy inewave/ --strict`** to verify no new errors appeared.

6. **Narrow remaining `# type: ignore` comments.** For each remaining bare ignore:
   - Run `mypy <file> --strict --show-error-codes` to find the specific code
   - Replace `# type: ignore` with `# type: ignore[code]  # explanation`

7. **Investigate removable ignores.** For each remaining ignore:
   - If the fix is a simple `cast()` or `assert isinstance()`, apply it
   - If the fix is complex or reduces readability, keep the narrowed ignore

8. **Run full test suite** and final `mypy inewave/ --strict` check.

### Key Files to Modify

Files with the most `# type: ignore` comments (in order of comment count):

- `inewave/newave/modelos/pmo.py` -- 19 comments
- `benchmarks/profile_read.py` -- 12 comments (not in inewave/ but in the project)
- `inewave/newave/modelos/parp.py` -- 11 comments
- `inewave/newave/modelos/parpvaz.py` -- 9 comments
- `inewave/newave/modelos/parpeol.py` -- 8 comments
- `inewave/newave/modelos/sistema.py` -- 7 comments
- `inewave/newave/modelos/patamar.py` -- 6 comments
- `inewave/newave/modelos/curva.py` -- 4 comments
- `inewave/newave/modelos/cvar.py` -- 4 comments
- `inewave/newave/modelos/re.py` -- 4 comments
- `inewave/newave/modelos/agrint.py` -- 4 comments
- `inewave/newave/modelos/penalid.py` -- 4 comments
- Plus ~100 single-comment files (mostly import-level pandas/numpy ignores)

Note: `benchmarks/profile_read.py` has 12 `# type: ignore` comments. This is outside `inewave/` but within the project. Decide whether to include it in scope. Recommendation: include it for consistency, but it is optional.

### Patterns to Follow

- **Always use specific error codes**: `# type: ignore[assignment]`, not `# type: ignore`
- **Always add explanation**: `# type: ignore[index]  # numpy 2D slice narrowing`
- **Import-level ignores**: Simply remove them. Do not replace with specific codes.
- **numpy slice pattern** (`tabela[:i, :]`): If mypy flags it, use `# type: ignore[index]  # numpy 2D array slice` or add a `cast()` if the expression is simple enough
- **cfinterface `data` access**: `self.data[N]` returns `Any` from cfinterface. Under `warn_return_any = false`, this does not need `# type: ignore`. If any remain, they are from a different error code.

### Pitfalls to Avoid

- **Do NOT run this ticket before tickets 023-024 are complete.** The set of `unused-ignore` comments depends entirely on the strict mode configuration.
- **Do NOT blindly remove all `# type: ignore` comments.** Some are genuinely needed. Only remove those flagged as `unused-ignore` by mypy.
- **Do NOT add `cast()` everywhere.** Use it only when the cast is trivially correct and the code remains readable. Excessive casting is worse than narrowed ignores.
- **Do NOT modify `benchmarks/` files** if they are outside the mypy strict scope. The mypy overrides may not cover `benchmarks/`.
- **The 2 existing `# type: ignore[arg-type]`** in `TabelaSerieAnual` and `TabelaSeriePatamarAnual` (line `df["ano"] = int(self._ano)`) are likely still needed. Verify but do not remove without understanding the underlying type issue.
- **`inewave/nwlistop/modelos/gtert.py`** has `# type: ignore` on import and DATA_LINE construction. The DATA_LINE one (`[...] + [FloatField(...) for i in ...] # type: ignore`) may be needed because the list concatenation produces `List[IntegerField | LiteralField | FloatField]` which may not match `List[Field]` exactly. Check with mypy.

## Testing Requirements

### Unit Tests

No new tests. Run the existing 1134 tests to confirm no regressions.

### Integration Tests

Run `mypy inewave/ --strict` as part of the verification step. Must report 0 errors.

### E2E Tests (if applicable)

Not applicable.

## Dependencies

- **Blocked By**: ticket-024 (strict mode must be fully active before cleanup)
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High -- the work is mechanical. Phase 1 (removing 189 import-level ignores) is a simple find-and-replace. Phase 2 (narrowing ~50 remaining ignores) requires running mypy per-file to identify error codes. Phase 3 (investigating removable ignores) is optional best-effort work with clear stopping criteria.
