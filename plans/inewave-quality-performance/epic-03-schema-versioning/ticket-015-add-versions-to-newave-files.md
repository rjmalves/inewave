# ticket-015 Add VERSIONS dictionaries to newave SectionFile classes

## Context

### Background

The newave module contains handler classes for NEWAVE input/output files. These handlers extend `SectionFile` (e.g., `Dger`, `Patamar`, `Sistema`, `Confhd`), `BlockFile` (e.g., `Pmo`, `Parp`, `Cvar`), or `RegisterFile` (e.g., `Hidr`, `Vazoes`, `Modif`). Currently only one newave file has `VERSIONS`: `avl_cortesfpha_nwv.py` (a deprecated `ArquivoCSV` / `BlockFile`).

The cfinterface framework provides a `VERSIONS` class-level dictionary that maps version key strings to component (section/block/register) type lists. When `read(content, version="29.2")` is called, `resolve_version()` performs lexicographic comparison to find the most recent version key `<=` the requested key and uses that component list instead of the default `SECTIONS`/`BLOCKS`/`REGISTERS` list. This is already implemented in cfinterface's `SectionFile.read()`, `BlockFile.read()`, and `RegisterFile.read()` methods -- no changes to cfinterface are needed.

This ticket adds `VERSIONS` dictionaries to newave handler classes identified in the version catalog (ticket-014). The catalog specifies which files vary, what changes, and what version keys to use.

### Relation to Epic

This is one of two implementation tickets (along with ticket-016 for nwlistop) that form the core of Epic 03. Together, they ensure `read(version=...)` works for all version-sensitive files across the codebase.

### Current State

- cfinterface 1.9.0 `SectionFile` supports `VERSIONS: Dict[str, List[Type[Section]]] = {}` and `read(content, version=...)`. See `/home/rogerio/git/cfinterface/cfinterface/files/sectionfile.py`.
- cfinterface 1.9.0 `BlockFile` supports `VERSIONS: Dict[str, List[Type[Block]]] = {}` and `read(content, version=...)`. See `/home/rogerio/git/cfinterface/cfinterface/files/blockfile.py`.
- cfinterface 1.9.0 `RegisterFile` supports `VERSIONS: Dict[str, List[Type[Register]]] = {}` and `read(content, version=...)`. See `/home/rogerio/git/cfinterface/cfinterface/files/registerfile.py`.
- The `resolve_version()` function in `/home/rogerio/git/cfinterface/cfinterface/versioning.py` does lexicographic `<=` comparison on sorted keys.
- newave `Dger` (SectionFile) has ~107 sections in its `SECTIONS` list. Version differences typically mean that certain sections are added/removed between NEWAVE versions (e.g., newer versions add sections for new features).
- newave `Pmo` (BlockFile) has ~22 blocks in its `BLOCKS` list. Some output blocks changed format between versions.
- newave `Parp` (BlockFile) has a complex block structure for autoregressive parameters.
- Only `avl_cortesfpha_nwv.py` currently has VERSIONS in the newave module.

## Specification

### Requirements

1. **Read the version catalog** produced by ticket-014 at `plans/inewave-quality-performance/version-catalog.md` to get the definitive list of newave files that need `VERSIONS`.
2. **For each newave handler identified in the catalog**, add a `VERSIONS` class-level dictionary mapping version keys to component type lists, following the existing pattern.
3. **Create version-variant model classes** where needed (e.g., if `Dger` needs different section classes for v28 vs v29, create the variant section classes in the model file).
4. **The default `SECTIONS`/`BLOCKS`/`REGISTERS` list must remain the "latest" version**, consistent with the pattern used in nwlistop files (e.g., `Cmarg.BLOCKS` is the latest format, `Cmarg.VERSIONS["27"]` is the older format).
5. **Do not modify existing model class behavior** -- version-variant classes should be new classes that differ only in their field definitions, inheriting from the same base.
6. **Import ordering convention**: cfinterface imports first, then inewave imports, following the convention established in Epic 02 learnings.

### Inputs/Props

- The version catalog at `plans/inewave-quality-performance/version-catalog.md` (produced by ticket-014)
- Existing newave handler files in `inewave/newave/`
- Existing newave model files in `inewave/newave/modelos/`
- cfinterface base class API (read-only reference)

### Outputs/Behavior

For each affected handler file:

```python
# Example for a SectionFile handler (pattern from avl_cortesfpha_nwv.py):
class SomeHandler(SectionFile):
    SECTIONS = [SectionA, SectionB_latest]  # latest/default
    VERSIONS = {
        "28": [SectionA, SectionB_v28],      # older format
        "29.2": [SectionA, SectionB_latest],  # matches default
    }
```

```python
# Example for a BlockFile handler (pattern from Pmo):
class SomeHandler(BlockFile):
    BLOCKS = [BlockA, BlockB_latest]  # latest/default
    VERSIONS = {
        "28": [BlockA, BlockB_v28],
        "29.4.1": [BlockA, BlockB_latest],
    }
```

After this ticket, calling `SomeHandler.read(path, version="28")` resolves to the v28 component list, while `SomeHandler.read(path)` (no version) uses the default list.

### Error Handling

- If a version key is requested that is older than all defined keys, `resolve_version()` returns `None` and cfinterface falls back to the default component list with a warning. No custom error handling needed.
- For newave `RegisterFile` subclasses (Hidr, Vazoes, Modif), the pattern is identical: add `VERSIONS: Dict[str, List[Type[Register]]] = { ... }`.

## Acceptance Criteria

- [ ] Given the version catalog lists N newave files as needing VERSIONS, when inspecting the modified handler files, then all N files have a `VERSIONS` dictionary with the version keys specified in the catalog.
- [ ] Given a newave handler with VERSIONS, when calling `Handler.read(path, version="<oldest_key>")` with appropriate test data, then the read uses the version-specific component list (verified by inspecting the parsed data structure).
- [ ] Given a newave handler with VERSIONS, when calling `Handler.read(path)` (no version argument), then the default `SECTIONS`/`BLOCKS` list is used (backward compatible).
- [ ] Given a newave handler with VERSIONS, when calling `Handler.read(path, version="99.0")` (version newer than all keys), then `resolve_version()` returns the latest defined version's components (not `None`), because `"99.0"` is `>=` all keys.
- [ ] Given no behavioral changes to existing code paths, when running `pytest`, then the full test suite (1126+ tests) passes.
- [ ] Given each new version-variant model class, when inspecting it, then it declares `__slots__ = []` and follows the naming conventions established in existing model files (e.g., `FooAnos27`, `FooAnos_v29_2`).

## Implementation Guide

### Suggested Approach

1. Read the version catalog (`plans/inewave-quality-performance/version-catalog.md`) to get the exact list of newave files to modify.
2. For each file in the catalog's "newave SectionFile" section:
   a. Open the handler file (e.g., `inewave/newave/dger.py`)
   b. Open its model files (e.g., `inewave/newave/modelos/dger.py`)
   c. Create version-variant section classes in the model file if needed
   d. Add `VERSIONS` dictionary to the handler class
   e. Import the version-variant classes in the handler file
3. For each file in the catalog's "newave BlockFile" section:
   a. Same process, but with Block classes and `BLOCKS`/`VERSIONS`
4. For each file in the catalog's "newave RegisterFile" section (if any):
   a. Same process, but with Register classes and `REGISTERS`/`VERSIONS`
5. Run `pytest` to verify no regressions.
6. Run `ruff check inewave/newave/` and `ruff format inewave/newave/` to ensure code quality.

### Key Files to Modify

The exact list comes from the ticket-014 catalog. Expected candidates based on codebase analysis:

- `inewave/newave/dger.py` and `inewave/newave/modelos/dger.py` -- Dger has ~107 sections; newer NEWAVE versions add new sections
- `inewave/newave/pmo.py` and `inewave/newave/modelos/pmo.py` -- Pmo output format varies between versions
- `inewave/newave/patamar.py` and `inewave/newave/modelos/patamar.py` -- patamar format may differ
- `inewave/newave/sistema.py` and `inewave/newave/modelos/sistema.py` -- subsystem configuration varies
- Other handlers as specified in the catalog

### Patterns to Follow

- **Pattern from `inewave/nwlistop/cmarg.py`**: `BLOCKS` is the default (latest) list. `VERSIONS` maps older version keys to their specific lists:
  ```python
  BLOCKS = [Submercado, CmargsAnos]  # latest
  VERSIONS = {
      "27": [Submercado, CmargsAnos27],  # older format
      "29.4.1": [Submercado, CmargsAnos],  # same as latest
  }
  ```
- **Pattern from `inewave/newave/avl_cortesfpha_nwv.py`**: Same approach for BlockFile:
  ```python
  BLOCKS = [VersaoModeloLibs, TabelaAvlCortesFpha]  # latest
  VERSIONS = {
      "28": [VersaoModelo, TabelaAvlCortesFpha28],
      "28.16": [VersaoModeloLibs, TabelaAvlCortesFpha],
  }
  ```
- **Version-variant class naming**: Use suffix `_v<major>_<minor>` (e.g., `PivarmAnos_v29_2`) or just version number suffix (e.g., `CmargsAnos27`, `CmargsAnos28`). Follow whatever convention is already used in the model file.
- **`__slots__ = []`** on every new model class.
- **Import ordering**: cfinterface imports first, then inewave imports.

### Pitfalls to Avoid

- **Do not use `set_version()`** -- it is deprecated and mutates the class-level `BLOCKS`/`SECTIONS` attribute globally. The new pattern uses `read(content, version=...)` which is instance-safe.
- **Do not change the default `SECTIONS`/`BLOCKS` list** -- it must remain the latest format for backward compatibility.
- **SectionFile `SECTIONS` order matters** -- sections are matched positionally in the file. Changing order can break parsing.
- **Lexicographic key comparison** -- `"28.12"` < `"28.16"` < `"28.2"` lexicographically. The existing codebase already accounts for this. Use keys consistent with the existing convention.
- **Dger has ~107 sections** -- version differences may only affect a subset. The VERSIONS dict still needs the complete section list for each version, not just the changed sections.

## Testing Requirements

### Unit Tests

Existing tests must pass. No new tests in this ticket -- ticket-018 handles version-aware testing.

### Integration Tests

Not applicable.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-014 (provides the version catalog)
- **Blocks**: ticket-017, ticket-018

## Effort Estimate

**Points**: 3
**Confidence**: Medium (exact scope depends on ticket-014 catalog size)
