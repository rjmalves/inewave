# ticket-001 Bump cfinterface dependency to >= 1.9.0

## Context

### Background

The cfinterface library has been revamped to v1.9.0 with significant new features: `StorageType` enum, `TabularSection`/`TabularParser`, schema versioning (`VERSIONS`, `read(version=...)`, `validate()`), `read_many()` batch API, compiled regex caching, array-backed data containers, and optimized FloatField writes. The inewave repository currently depends on `cfinterface >= 1.8.0` and must be updated to unlock these features.

### Relation to Epic

This is the foundational ticket for Epic 01. All subsequent work in this plan depends on the cfinterface >= 1.9.0 dependency being available. It must be completed first.

### Current State

- `pyproject.toml` line 9: `"cfinterface>=1.8.0"`
- `inewave/__init__.py` line 9: `__version__ = "1.12.0"`

## Specification

### Requirements

1. Update the cfinterface dependency version bound in `pyproject.toml` from `>= 1.8.0` to `>= 1.9.0`
2. Bump the inewave version in `inewave/__init__.py` from `"1.12.0"` to `"1.13.0"` (minor version bump to signal the new dependency floor)
3. Verify that `uv sync --all-extras --dev` resolves successfully with cfinterface >= 1.9.0

### Inputs/Props

None -- this is a configuration change.

### Outputs/Behavior

- `pyproject.toml` has `"cfinterface>=1.9.0"` in the `dependencies` array
- `inewave/__init__.py` has `__version__ = "1.13.0"`
- `uv sync` resolves without errors

### Error Handling

If cfinterface v1.9.0 is not yet published to PyPI, install from the local path or git reference instead:

```
"cfinterface @ file:///home/rogerio/git/cfinterface"
```

Revert to `"cfinterface>=1.9.0"` once published.

## Acceptance Criteria

- [ ] Given `pyproject.toml`, when I read line 9, then it contains `"cfinterface>=1.9.0"`
- [ ] Given `inewave/__init__.py`, when I read it, then `__version__` is `"1.13.0"`
- [ ] Given a fresh virtual environment, when I run `uv sync --all-extras --dev`, then it completes without dependency resolution errors
- [ ] Given the installed environment, when I run `python -c "import cfinterface; print(cfinterface.__version__)"`, then it prints a version >= 1.9.0

## Implementation Guide

### Suggested Approach

1. Edit `pyproject.toml`: change `"cfinterface>=1.8.0"` to `"cfinterface>=1.9.0"` on line 9
2. Edit `inewave/__init__.py`: change `__version__ = "1.12.0"` to `__version__ = "1.13.0"` on line 9
3. Run `uv sync --all-extras --dev` to verify dependency resolution
4. Run `python -c "from cfinterface.storage import StorageType; print(StorageType.BINARY)"` to verify the new API is available

### Key Files to Modify

- `/home/rogerio/git/inewave/pyproject.toml` (line 9)
- `/home/rogerio/git/inewave/inewave/__init__.py` (line 9)

### Patterns to Follow

- Keep all other dependencies unchanged
- Do not modify any `[tool.*]` sections in pyproject.toml

### Pitfalls to Avoid

- Do NOT bump to `== 1.9.0` (pinned) -- keep `>=` for forward compatibility
- Do NOT change the Python version requirement (`>= 3.10`)
- Do NOT modify the `[project.optional-dependencies]` dev group

## Testing Requirements

### Unit Tests

None needed -- this is a dependency version bump.

### Integration Tests

Run `uv sync --all-extras --dev` and verify cfinterface >= 1.9.0 is installed.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: None (first ticket)
- **Blocks**: ticket-002, ticket-003

## Effort Estimate

**Points**: 1
**Confidence**: High
