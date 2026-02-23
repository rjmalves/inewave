# inewave Quality and Performance Upgrade

## Overview

Progressive plan to upgrade inewave (v1.12.0 -> v1.13.0) to leverage cfinterface v1.9.0 features: StorageType enum, TabularSection parser, schema versioning, and performance optimizations.

## Tech Stack

- Python 3.10+
- cfinterface >= 1.9.0
- numpy >= 2.2.1, pandas >= 2.2.3
- Build: Hatchling + uv
- Quality: ruff, mypy, pytest + coverage, sphinx

## Epics

| Epic | Name                                 | Tickets       | Status    |
| ---- | ------------------------------------ | ------------- | --------- |
| 01   | Foundation and StorageType Migration | 3 (detailed)  | completed |
| 02   | nwlistop TabularSection Adoption     | 10 (detailed) | completed |
| 03   | Schema Versioning                    | 5 (refined)   | completed |
| 04   | Performance Optimization             | 4 (refined)   | completed |
| 05   | Quality and Type Safety              | 4 (refined)   | completed |
| 06   | Testing Improvements                 | 4 (outline)   | pending   |
| 07   | Documentation                        | 3 (outline)   | pending   |

## Progress Tracking

| Ticket     | Title                                                                          | Epic    | Status    | Detail Level |
| ---------- | ------------------------------------------------------------------------------ | ------- | --------- | ------------ |
| ticket-001 | Bump cfinterface dependency to >= 1.9.0                                        | epic-01 | completed | Detailed     |
| ticket-002 | Migrate STORAGE string literals to StorageType enum                            | epic-01 | completed | Detailed     |
| ticket-003 | Verify full test suite and fix regressions                                     | epic-01 | completed | Detailed     |
| ticket-004 | Design and implement TabelaSerieAnual base class                               | epic-02 | completed | Detailed     |
| ticket-005 | Design and implement TabelaSeriePatamarAnual base class                        | epic-02 | completed | Detailed     |
| ticket-006 | Migrate ValoresSerie archive base classes                                      | epic-02 | completed | Detailed     |
| ticket-007 | Migrate ValoresSeriePatamar archive base classes                               | epic-02 | completed | Detailed     |
| ticket-008 | Batch migrate ArquivoREE and ArquivoSIN models (35 files)                      | epic-02 | completed | Detailed     |
| ticket-009 | Batch migrate ArquivoUsina models (17 files)                                   | epic-02 | completed | Detailed     |
| ticket-010 | Batch migrate ArquivoSubmercadoPatamar and ArquivoREEPatamar models (47 files) | epic-02 | completed | Detailed     |
| ticket-011 | Batch migrate ArquivoSINPatamar and ArquivoUsinaPatamar models (47 files)      | epic-02 | completed | Detailed     |
| ticket-012 | Batch migrate remaining archive types (16 files)                               | epic-02 | completed | Detailed     |
| ticket-013 | Clean up deprecated block classes and verify                                   | epic-02 | completed | Detailed     |
| ticket-014 | Survey and catalog version-dependent formats                                   | epic-03 | completed | Refined      |
| ticket-015 | Add VERSIONS to newave SectionFile classes                                     | epic-03 | completed | Refined      |
| ticket-016 | Add VERSIONS to nwlistop BlockFile classes                                     | epic-03 | completed | Refined      |
| ticket-017 | Add validate() integration to versioned files                                  | epic-03 | completed | Refined      |
| ticket-018 | Write version-aware tests for versioned files                                  | epic-03 | completed | Refined      |
| ticket-019 | Profile inewave read operations                                                | epic-04 | completed | Refined      |
| ticket-020 | Optimize DataFrame creation in archive bases                                   | epic-04 | completed | Refined      |
| ticket-021 | Implement lazy imports for nwlistop                                            | epic-04 | completed | Refined      |
| ticket-022 | Create benchmark suite for read performance                                    | epic-04 | completed | Refined      |
| ticket-023 | Enable mypy strict mode for newave module                                      | epic-05 | completed | Refined      |
| ticket-024 | Fix mypy strict mode errors in nwlistop                                        | epic-05 | completed | Refined      |
| ticket-025 | Reduce code duplication in nwlistop archives                                   | epic-05 | completed | Refined      |
| ticket-026 | Clean up type ignore comments                                                  | epic-05 | completed | Refined      |
| ticket-027 | Add round-trip tests for newave handlers                                       | epic-06 | pending   | Outline      |
| ticket-028 | Add round-trip tests for nwlistop handlers                                     | epic-06 | pending   | Outline      |
| ticket-029 | Add version-aware and validation tests                                         | epic-06 | pending   | Outline      |
| ticket-030 | Optimize test execution                                                        | epic-06 | pending   | Outline      |
| ticket-031 | Write migration guide for downstream users                                     | epic-07 | pending   | Outline      |
| ticket-032 | Update API documentation and docstrings                                        | epic-07 | pending   | Outline      |
| ticket-033 | Add performance benchmarks to documentation                                    | epic-07 | pending   | Outline      |
