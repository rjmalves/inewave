# ticket-017 Add validate() integration to versioned file classes

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Wire up cfinterface's `validate()` method on all file classes that now have `VERSIONS` dictionaries (from tickets 015-016). This enables downstream consumers to call `file.validate(version="v30")` to check whether a read file matches the expected version format, producing a `VersionMatchResult` with matched/missing/unexpected type information.

## Anticipated Scope

- **Files likely to be modified**: All handler files that received VERSIONS in tickets 015-016 (no new classes needed -- `validate()` is inherited from cfinterface base classes)
- **Key decisions needed**: Whether to add convenience wrapper methods or rely on the inherited `validate()` signature; whether to add automatic validation warnings on read
- **Open questions**:
  - Does the inherited `validate()` from cfinterface work correctly with the inewave block/section types, or does it need customization?
  - Should validation be opt-in only (consistent with cfinterface convention) or should warnings be emitted automatically?
  - What threshold value should be used for the default_ratio in `validate_version()`?

## Dependencies

- **Blocked By**: ticket-015, ticket-016
- **Blocks**: ticket-018

## Effort Estimate

**Points**: 2
**Confidence**: Low (will be re-estimated during refinement)
