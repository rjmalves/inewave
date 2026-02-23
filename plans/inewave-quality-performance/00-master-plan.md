# Master Plan: inewave Quality and Performance Upgrade

## Executive Summary

Upgrade the inewave repository (v1.12.0, 542 Python files, ~514K LOC total) to fully leverage the cfinterface v1.9.0 revamp. This plan covers seven epics: dependency upgrade with StorageType migration, nwlistop TabularSection adoption (the single biggest win -- targeting ~150 files and potentially eliminating tens of thousands of lines of boilerplate), schema versioning for NEWAVE version evolution, performance optimization, code quality and type safety, test improvements, and documentation updates.

## Goals and Non-Goals

### Goals

1. **Eliminate deprecation warnings**: Replace all 16 `STORAGE = "BINARY"` string literals with `StorageType.BINARY` and bump cfinterface dependency to >= 1.9.0
2. **Reduce nwlistop boilerplate**: Migrate ~160+ model files (ValoresSerie/ValoresSeriePatamar subclasses) and 13 archive base classes to use `TabularSection`, potentially removing 15K-30K lines of manual parsing
3. **Enable version-aware reads**: Add `VERSIONS` dictionaries to file classes where NEWAVE format varies across versions (currently only 5 files have VERSIONS)
4. **Improve runtime performance**: Leverage cfinterface's compiled regex, array-backed containers, and optimized FloatField; profile and optimize inewave-specific bottlenecks
5. **Strengthen type safety**: Move toward mypy strict mode, add proper type annotations, reduce `# type: ignore` usage
6. **Improve test quality**: Add round-trip tests, version-aware tests, and validation tests; improve test execution speed
7. **Update documentation**: Migration guide for downstream users, updated API reference, performance benchmarks

### Non-Goals

- Changing the public API surface (all changes must be backward-compatible)
- Rewriting the newave/nwlistcf modules from scratch
- Adding async file I/O support
- Dropping Python 3.10 support
- Removing pandas as a dependency (inewave legitimately depends on DataFrames)

## Architecture Overview

### Current State

```
inewave/
  newave/          # 76 handlers (52 SectionFile, 11 BlockFile, 3 RegisterFile) + 74 models
  nwlistop/        # 150+ handlers + 196 models (all BlockFile subclasses)
    modelos/
      blocos/      # 10 base block types (ValoresSerie, ValoresSeriePatamar, etc.)
      arquivos/    # 13 base archive types (ArquivoREE, ArquivoSIN, etc.)
  nwlistcf/        # 5 handlers + models
  libs/            # 3 high-level interfaces + models
  _utils/          # Formatting helpers
  config.py        # Constants (MAX_SERIES, MESES, etc.)
```

**Key patterns**:

- `STORAGE = "BINARY"` used as string literal in 16 RegisterFile/SectionFile subclasses
- nwlistop uses 2 base block classes (`ValoresSerie`, `ValoresSeriePatamar`) plus 1 special (`ValoresClasseTermicaSeriePatamar`), each with manual `numpy` + `pandas` DataFrame construction in `read()`
- 13 archive base classes in `nwlistop/modelos/arquivos/` all implement identical `__monta_tabela()` with `pd.concat` loop
- Only 5 files currently declare `VERSIONS` dictionaries
- Tests use mock data via `tests/mocks/` with `unittest.mock.patch` on `builtins.open`

### Target State

```
inewave/
  newave/          # Same structure, STORAGE = StorageType.BINARY, VERSIONS on key files
  nwlistop/        # Same handlers, but models use TabularSection subclasses
    modelos/
      blocos/      # Simplified -- many replaced by TabularSection subclasses
      arquivos/    # Simplified -- base classes leverage TabularSection
  nwlistcf/        # Minor updates (StorageType, typing)
  libs/            # Unchanged
  _utils/          # Unchanged
  config.py        # Unchanged
```

**Key improvements**:

- All `STORAGE` attributes use `StorageType` enum
- nwlistop model blocks are `TabularSection` subclasses with `COLUMNS = [ColumnDef(...)]`
- Archive base classes (ArquivoREE, etc.) simplified to delegate to `TabularSection.data`
- Version-sensitive files declare `VERSIONS` dictionaries
- mypy strict mode passing
- Comprehensive round-trip and version-aware tests

### Key Design Decisions

1. **Module-by-module migration**: The StorageType migration is small (16 files) and done in one ticket. The TabularSection migration is massive and must be batched by archive type.
2. **Preserve backward compatibility**: All public properties (`.valores`, `.cadastro`, `.ree`, etc.) must continue to return the same types and column names.
3. **Bottom-up epic ordering**: Foundation first (cfinterface bump), then the biggest ROI (nwlistop TabularSection), then versioning, then quality/perf/testing/docs.
4. **TabularSection migration strategy**: Replace the `ValoresSerie`/`ValoresSeriePatamar` block hierarchy with `TabularSection` subclasses. The 13 archive base classes then simplify because `TabularSection.data` provides the dict-of-lists directly, which can be converted to DataFrame via `TabularParser.to_dataframe()`.

## Technical Approach

### Tech Stack

- **Language**: Python 3.10+
- **Dependencies**: cfinterface >= 1.9.0, numpy >= 2.2.1, pandas >= 2.2.3
- **Build**: Hatchling + uv
- **CI**: GitHub Actions (Python 3.10, 3.11, 3.12)
- **Quality**: ruff (80 char line length), mypy, pytest + coverage, sphinx

### Component/Module Breakdown

| Module      | Files                     | Migration Scope                                   |
| ----------- | ------------------------- | ------------------------------------------------- |
| `newave/`   | 76 handlers, 74 models    | 16 STORAGE migrations, VERSIONS on ~10 files      |
| `nwlistop/` | 150+ handlers, 196 models | Full TabularSection migration, VERSIONS expansion |
| `nwlistcf/` | 5 handlers                | Minor typing updates                              |
| `libs/`     | 3 interfaces              | Unchanged                                         |

### nwlistop File Distribution by Base Class

| Base Archive Class                                | Count    | Block Type Used                    |
| ------------------------------------------------- | -------- | ---------------------------------- |
| `ArquivoSubmercadoPatamar` (+ Submercado variant) | 35       | `ValoresSeriePatamar`              |
| `ArquivoUsinaPatamar`                             | 25       | `ValoresSeriePatamar`              |
| `ArquivoSINPatamar`                               | 22       | `ValoresSeriePatamar`              |
| `ArquivoSIN`                                      | 19       | `ValoresSerie`                     |
| `ArquivoUsina`                                    | 17       | `ValoresSerie`                     |
| `ArquivoREE`                                      | 16       | `ValoresSerie`                     |
| `ArquivoREEPatamar`                               | 12       | `ValoresSeriePatamar`              |
| `ArquivoRestricaoPatamar`                         | 8        | `ValoresSeriePatamar`              |
| `ArquivoRestricao`                                | 4        | `ValoresSerie`                     |
| `ArquivoClasseTermicaSubmercadoPatamar`           | 1        | `ValoresClasseTermicaSeriePatamar` |
| `ArquivoEstacaoBombeamentoPatamar`                | 2        | `ValoresSeriePatamar`              |
| `ArquivoPARSubmercadoPatamar`                     | 1        | `ValoresSeriePatamar`              |
| **Total**                                         | **~162** |                                    |

### Data Flow

```
File on disk
    |
    v
cfinterface BlockFile.read() -- uses regex cache, array-backed containers
    |
    v
Block.read() / TabularSection.read() -- parses lines into dict-of-lists
    |
    v
Archive base class (.valores property) -- converts to pd.DataFrame via TabularParser.to_dataframe()
    |
    v
User code (downstream consumers like sintetizador-newave)
```

### Testing Strategy

- **Unit tests**: Each migrated model file gets a round-trip test (read -> write -> read)
- **Integration tests**: Archive-level tests verify `.valores` DataFrame shape, dtypes, and values
- **Regression tests**: Existing mock-based tests must pass without modification
- **Version tests**: Version-aware reads with `version=` parameter
- **Validation tests**: `validate()` calls on version-declared files

## Phases and Milestones

| Epic | Name                                 | Scope                                               | Duration Estimate |
| ---- | ------------------------------------ | --------------------------------------------------- | ----------------- |
| 1    | Foundation and StorageType Migration | Bump cfinterface, migrate 16 STORAGE literals       | 1-2 weeks         |
| 2    | nwlistop TabularSection Adoption     | Migrate ~162 model files + 13 base classes          | 4-6 weeks         |
| 3    | Schema Versioning                    | Add VERSIONS to version-sensitive files             | 2-3 weeks         |
| 4    | Performance Optimization             | Profile, optimize DataFrame creation, lazy imports  | 2-3 weeks         |
| 5    | Quality and Type Safety              | mypy strict, type annotations, deduplication        | 2-3 weeks         |
| 6    | Testing Improvements                 | Round-trip tests, version tests, parallel execution | 2-3 weeks         |
| 7    | Documentation                        | Migration guide, API reference, benchmarks          | 1-2 weeks         |

## Risk Analysis

| Risk                                                | Probability | Impact | Mitigation                                                                                                                                       |
| --------------------------------------------------- | ----------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| TabularSection cannot handle all nwlistop formats   | Low         | High   | Analyze all 3 base block types before starting; TabularSection already handles the exact inewave conventions (END_PATTERN, blank-line detection) |
| Downstream breakage (sintetizador-newave)           | Medium      | High   | Preserve all public property signatures and DataFrame column names; version bump with changelog                                                  |
| Test mock data incompatible with TabularSection     | Medium      | Medium | Update mock data format only if needed; existing tests remain primary regression gate                                                            |
| Performance regression from TabularSection overhead | Low         | Medium | Benchmark before/after; TabularParser uses the same Field/Line infrastructure                                                                    |

## Success Metrics

1. Zero `STORAGE = "TEXT"` or `STORAGE = "BINARY"` string literals remaining
2. nwlistop model files reduced by 30-50% in LOC through TabularSection adoption
3. All 430+ existing tests pass without modification
4. mypy strict mode passes on all modules
5. At least 10 file classes have `VERSIONS` dictionaries
6. Documented migration guide for downstream users
7. No performance regression on benchmark suite (read 100 typical files)
