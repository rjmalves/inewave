# Epic 03 Learnings: Schema Versioning for NEWAVE Version Evolution

## Patterns Established

- **Zero new VERSIONS needed**: The version catalog revealed that all confirmed format differences are already handled by the existing 5 versioned files (cmarg, cmargmed, pivarm, pivarmincr, avl_cortesfpha_nwv). No additional files require VERSIONS dictionaries beyond these 5. See `plans/inewave-quality-performance/version-catalog.md` for the comprehensive analysis.
- **Graceful degradation for unconfirmed variants**: Files with suspected version differences (dger, pmo, patamar, sistema) degrade gracefully because they use keyword-based matching in their section/block definitions. Missing sections/blocks simply return None rather than raising parse errors.
- **Lexicographic version key comparison**: Version keys are compared lexicographically, not as semantic versions. `"28.12"` < `"28.16"` < `"28.2"` because string comparison is character-by-character from left to right. This convention is embedded in the version-catalog.md document. See `cfinterface/cfinterface/versioning.py` for the resolve_version() implementation.
- **validate() is inherited, no implementation needed**: cfinterface's inherited `validate()` method on BlockFile/SectionFile works correctly with inewave block/section types without modification. The method checks whether parsed data matches expected component types for a given version. See ticket-017 findings.

## Architectural Decisions

- **VERSIONS declarations are complete as-is**: After survey and implementation, no modifications to VERSIONS dictionaries were needed beyond what already existed. The architecture already correctly handles all known format variants.
- **No detect_version() helper added**: The inherited `validate()` API is sufficient for downstream consumers. A `detect_version()` helper was evaluated in ticket-017 but determined unnecessary because version information is typically known from the NEWAVE model run context. Instead, users can call `handler.validate(version="known_version")` directly.
- **Test migration from set_version() to read(version=...)**: All existing version-aware tests were migrated from the deprecated `set_version()` class-level mutation API to the modern instance-safe `read(path, version=...)` API. This eliminates test ordering issues and makes version selection explicit at the call site.
- **Version key strategy documented in version-catalog.md**: Rather than adding inline documentation scattered across source files, the version catalog centralizes all versioning strategy information. Future maintainers reference this document to understand which files are versioned, what changes between versions, and why no additional VERSIONS were needed.

## Files & Structures Created

- `plans/inewave-quality-performance/version-catalog.md`: 417-line comprehensive catalog documenting all 5 already-versioned files, their version keys, what changes between versions, the lexicographic key convention, the decision that 0 new nwlistop files need VERSIONS, the decision that 0 newave files need VERSIONS, 4 open questions for unconfirmed variants, and detailed analysis organized by file type (already versioned, nwlistop BlockFile, newave SectionFile, newave BlockFile, newave RegisterFile, no versioning needed). This is a complete audit trail for the schema versioning state of the codebase.
- 8 new validate() tests across multiple test files verifying that `handler.validate(version=correct_key)` returns `matched=True` and `handler.validate(version=wrong_key)` returns `matched=False` or has non-empty `missing_types`. See ticket-018 test migrations in `tests/nwlistop/test_cmarg.py`, `test_cmargmed.py`, `test_pivarm.py`, `test_pivarmincr.py`, and `tests/newave/test_avl_cortesfpha_nwv.py`.

## Conventions Adopted

- **VERSIONS key naming**: Use NEWAVE version numbers as bare strings: `"27"`, `"28"`, `"28.12"`, `"28.16"`, `"29.2"`, `"29.4.1"`. No "v" prefix or semver formatting. Order keys in VERSIONS dict from oldest to newest for readability. See `inewave/nwlistop/cmarg.py` for a reference implementation.
- **read(version=...) call site convention**: Pass version as a keyword argument to the read() method rather than mutating class state. Pattern: `handler.read(path, version="27")` instead of `handler.set_version("27"); handler.read(path)`. This is now the standard across the test suite.
- **validate() convention for version checking**: Call `handler.validate(version=known_version)` to check if parsed data matches expected types for that version. The result is a `VersionMatchResult(matched: bool, missing_types: List, unexpected_types: List, default_ratio: float)`. See cfinterface's versioning.py for the VersionMatchResult definition.

## Surprises & Deviations

- **Survey found zero new VERSIONS needed**: The epic was scoped to "expand VERSIONS coverage to ~10-20 additional files" but the version catalog analysis revealed that all known format differences are already covered by the existing 5 files. This is not a scope reduction but an empirical finding: the codebase format evolution is simpler than anticipated, with version differences concentrated in a few files. The unconfirmed candidates (dger, pmo, patamar, sistema) likely degrade gracefully without explicit VERSIONS due to their section-based architecture.
- **No breaking changes to cfinterface API**: The implementation expected potential cfinterface API gaps and the need for custom helpers or wrappers, but cfinterface 1.9.0's VERSIONS and validate() implementations are fully sufficient. No inewave-specific code was needed to support versioning.
- **set_version() was genuinely deprecated**: The test migrations revealed that `set_version()` mutates the class-level BLOCKS attribute globally, causing test ordering issues and making version selection implicit rather than explicit. The new `read(version=...)` API avoids this entirely and the migration was straightforward (replace `set_version()` + `read()` with `read(..., version=...)` in one line).

## Recommendations for Future Epics

- **Before investigating dger/pmo/patamar/sistema**: Create test files from actual NEWAVE output of different versions (pre-v28, v28, v29.x) and attempt to parse them. Use `handler.validate()` to detect whether the default SECTIONS/BLOCKS list successfully parses older files. If `validate(version=None)` returns `matched=True` with low `default_ratio` on pre-v28 files, then VERSIONS is not needed. If `matched=False` or `default_ratio` is high, then VERSIONS should be added. This is the empirical way to confirm the "graceful degradation" hypothesis.
- **Reference the version-catalog.md in pull requests**: When reviewing code that touches versioning, reference the version-catalog.md to explain the version strategy. This centralizes institutional knowledge and prevents regressing to the old approach.
- **Use read(version=...) in all new tests**: The modern API is safer and more explicit. Do not reintroduce `set_version()` in any new code. Make this a linting rule or code review practice.
- **Validate at module boundaries**: If inewave users are uncertain of their input file format, encourage them to call `handler.validate(version=suspected_version)` to confirm before extracting data. Document this pattern in the migration guide (ticket-031).

## Key File References

- `plans/inewave-quality-performance/version-catalog.md`: Complete versioning audit and strategy document. 5 already-versioned files documented with version keys and format changes. 0 additional files identified as needing VERSIONS. Lexicographic version key convention explained. Open questions for suspected variants (dger, pmo, patamar, sistema) listed with rationale for deferral.
- `inewave/nwlistop/cmarg.py`: Reference handler with VERSIONS. Pattern: `BLOCKS = [Submercado, CmargsAnos]` (latest), `VERSIONS = { "27": [Submercado, CmargsAnos27], "29.4.1": [Submercado, CmargsAnos] }`. See lines 1-50 for full structure.
- `inewave/nwlistop/modelos/cmarg.py`: Reference model with version-variant classes. `CmargsAnos27` (FloatField 8-char width), `CmargsAnos` (FloatField 11-char width). Both extend `TabelaSeriePatamarAnual`, both declare `__slots__ = []`.
- `inewave/nwlistop/pivarm.py`: Handler with format-variant (not just width-variant) VERSIONS. Uses `format="E"` (scientific notation) vs decimal. Pattern: `FloatField(15, 7 + 15 * i, 2)` (decimal) vs `FloatField(15, 7 + 15 * i, 7, format="E")` (scientific). See model file `inewave/nwlistop/modelos/pivarm.py` for class definitions.
- `inewave/newave/avl_cortesfpha_nwv.py`: Reference newave BlockFile with VERSIONS. Pattern: `BLOCKS = [VersaoModeloLibs, TabelaAvlCortesFpha]` (latest). `VERSIONS` maps version keys to different block class combinations (different VersaoModelo types + table classes).
- `tests/nwlistop/test_cmarg.py`: Reference test file migrated from `set_version()` to `read(version=...)`. Pattern: `Cmarg.read(ARQ_TESTE, version="27")` instead of `Cmarg.set_version("27"); Cmarg.read(ARQ_TESTE)`. Include validate() tests: `n.validate(version="27")` should return `matched=True`.
- `tests/mocks/arquivos/cmarg.py`: Reference mock data file with version-specific mock constants. `MockCmarg27` (older format), `MockCmarg` (latest format). Each is a list of strings (lines) with the correct field widths for that version.
- `/home/rogerio/git/cfinterface/cfinterface/versioning.py`: Contains `resolve_version()` (lexicographic comparison logic) and `validate_version()` (type-matching logic). Reference for understanding how version keys are compared and how validation works.
