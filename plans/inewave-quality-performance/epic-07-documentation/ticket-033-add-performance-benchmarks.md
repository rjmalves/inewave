# ticket-033 Add performance benchmarks to documentation

## Context

### Background

Epic-04 (Performance Optimization) established a benchmark suite at `benchmarks/profile_read.py` and a regression benchmark runner that produces `benchmarks/benchmark_results.md`. These files exist and contain current results, but they are internal development artifacts with no user-facing documentation explaining what the benchmarks measure, how to interpret the results, or how to reproduce them. Downstream consumers and contributors have no visibility into the performance characteristics of inewave v1.13.0.

### Relation to Epic

This is the second deliverable of epic-07 (Documentation). It makes the performance work from epic-04 visible to users and provides a reference for future regression detection.

### Current State

- `benchmarks/benchmark_results.md` exists at `/home/rogerio/git/inewave/benchmarks/benchmark_results.md`. Contains three benchmark tables (Import, Read, Aggregation) with Mean, Delta, Median, Min, Max, Std Dev, and Peak Memory columns. Generated 2026-02-23. Uses 2 iterations with tracemalloc for memory.
- `benchmarks/profile_read.py` exists at `/home/rogerio/git/inewave/benchmarks/profile_read.py`. Contains phase-level profiling with monkey-patch instrumentation. Generates `benchmarks/profile_report.md`.
- `benchmarks/profile_report.md` exists at `/home/rogerio/git/inewave/benchmarks/profile_report.md`. Contains summary table (parsing %, DataFrame %, aggregation %), raw phase times, import times, per-file cProfile top-20, key findings, and recommendations.
- No `benchmarks/README.md` exists.
- No user-facing documentation page references the benchmarks.
- The `docs/source/index.rst` sphinx toctree has no performance/benchmarks section.
- `pyproject.toml` does not list benchmark dependencies (they reuse dev extras: pytest, plus standard library modules).

## Specification

### Requirements

1. **Create `benchmarks/README.md`** at `/home/rogerio/git/inewave/benchmarks/README.md` in Markdown format. This is a standalone document that serves as the entry point for anyone exploring the `benchmarks/` directory.

2. **Content of `benchmarks/README.md`**:
   - **Overview**: What the benchmarks measure (import time, read time for representative file types, aggregation time, memory usage).
   - **How to Run**: Step-by-step instructions for running both benchmark tools:
     - `python benchmarks/profile_read.py` (generates `profile_report.md`)
     - `python -m pytest benchmarks/ --benchmark` or the custom benchmark runner (generates `benchmark_results.md`)
   - **Interpreting Results**: Brief explanation of each table in `benchmark_results.md`:
     - Import Benchmarks: measures lazy import overhead
     - Read Benchmarks: end-to-end `Handler.read()` wall-clock time
     - Aggregation Benchmarks: `.valores` property access time after read
     - Delta column: change vs. previous baseline
     - Peak Memory: Python-level allocations via tracemalloc
   - **Key Performance Characteristics of v1.13.0**: A curated summary (not a copy-paste of the raw results) highlighting:
     - Lazy imports: `import inewave.nwlistop` takes ~5ms (was ~300ms before lazy imports)
     - Read performance: ~70ms for non-patamar files, ~210ms for patamar files (Cmarg), ~640ms for Pmo
     - Aggregation: `.valores` access is near-zero (~0.1ms) due to collect-then-concat optimization
     - Memory: 8-28 MB peak depending on file type
   - **Architecture**: Brief description of the profiling approach (monkey-patch instrumentation of `TabularParser.parse_lines`, `_build_dataframe`, `formata_df_meses_para_datas_nwlistop`, `__monta_tabela`)
   - **Files in this directory**: One-line description of each file (`benchmark_results.md`, `profile_read.py`, `profile_report.md`)

3. **Do NOT modify `benchmark_results.md` or `profile_report.md`** -- these are generated artifacts.

4. **Do NOT add a sphinx documentation page for benchmarks** -- the `benchmarks/README.md` is the sole documentation artifact. It is referenced from `MIGRATION.md` (ticket-031).

5. **Write in English** -- the benchmarks directory is developer-facing infrastructure, and the existing `profile_read.py` docstring and `benchmark_results.md` are already in English.

### Error Handling

Not applicable (documentation-only ticket).

## Acceptance Criteria

- [ ] Given no `benchmarks/README.md` exists, when this ticket is completed, then `/home/rogerio/git/inewave/benchmarks/README.md` exists with all sections listed above
- [ ] Given the README references `profile_read.py`, when this ticket is completed, then the "How to Run" section contains the exact command `python benchmarks/profile_read.py` and notes it must be run from the repository root
- [ ] Given the README contains a "Key Performance Characteristics" section, when this ticket is completed, then it includes quantified metrics for import time, read time, aggregation time, and memory, sourced from the current `benchmark_results.md`
- [ ] Given `benchmark_results.md` and `profile_report.md` are generated files, when this ticket is completed, then neither file has been modified
- [ ] Given the benchmarks directory is developer-facing, when this ticket is completed, then the README is written in English

## Implementation Guide

### Suggested Approach

1. Create `/home/rogerio/git/inewave/benchmarks/README.md`.
2. Write the Overview section explaining the benchmark suite's purpose.
3. Write the How to Run section with exact commands. Note that `profile_read.py` requires the repository root in `sys.path` (it imports from `tests/mocks/`). The script handles this itself when run as `__main__`.
4. Write the Interpreting Results section by reading `benchmark_results.md` and explaining each table and column.
5. Write the Key Performance Characteristics section by extracting the headline numbers from `benchmark_results.md` and `profile_report.md`. Focus on user-observable metrics (import time, read time), not internal phase breakdowns.
6. Write the Architecture section briefly describing the monkey-patch instrumentation approach.
7. Write the Files section listing each file in the directory with a one-line description.

### Key Files to Modify

- **Create**: `/home/rogerio/git/inewave/benchmarks/README.md`

### Patterns to Follow

- English language throughout (matching existing benchmark artifacts)
- Markdown format with tables for numeric data
- Reference file paths relative to the repository root (e.g., `benchmarks/profile_read.py`)
- Use the same table format as `benchmark_results.md` for any performance data tables

### Pitfalls to Avoid

- Do NOT copy-paste the entire `benchmark_results.md` into the README. The README should contain a curated summary and point to the generated files for full details.
- Do NOT run the benchmarks as part of this ticket. Use the existing results in `benchmark_results.md` as the data source.
- Do NOT add benchmark deps to `pyproject.toml`. The benchmark scripts use standard library (`time`, `cProfile`, `tracemalloc`) plus packages already in dev extras.
- The Delta column in `benchmark_results.md` shows change vs. a previous baseline. Do NOT interpret high Delta values as regressions without noting the context (the `import inewave` +48.8% is noise from cold-start variance with only 2 iterations).
- The `__monta_tabela` optimization (collect-then-concat) is invisible in benchmark results because mock data has only 1 year-block. Note this in the README: real-world improvement is significant for files with 20+ year blocks.

## Testing Requirements

### Unit Tests

Not applicable (documentation-only).

### Integration Tests

Not applicable (documentation-only).

### Manual Verification

- Read `benchmarks/README.md` and verify all sections are present
- Verify the "How to Run" commands are accurate
- Verify the performance numbers match the current `benchmark_results.md`
- Verify `benchmark_results.md` and `profile_report.md` are unmodified

## Dependencies

- **Blocked By**: None (benchmark artifacts from epic-04 are already complete)
- **Blocks**: None

## Effort Estimate

**Points**: 1
**Confidence**: High
