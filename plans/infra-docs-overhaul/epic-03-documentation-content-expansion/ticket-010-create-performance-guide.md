# ticket-010 Create Performance Guide Documentation Page

## Context

### Background

The inewave library includes a benchmark suite in `benchmarks/` that measures import times, file read times, and DataFrame aggregation times. The benchmark results and profiling data are documented in `benchmarks/benchmark_results.md` and `benchmarks/profile_report.md`, but this information is not exposed in the user-facing Sphinx documentation. Users who process hundreds of NWLISTOP output files need guidance on optimizing throughput and understanding performance characteristics.

### Relation to Epic

This is the third content-expansion ticket in Epic 3. It translates and adapts the technical benchmark documentation into a user-facing performance guide in Brazilian Portuguese. The page will be referenced from the updated toctree in ticket-012 and cross-referenced from the FAQ (ticket-009).

### Current State

- The benchmark suite lives in `benchmarks/` with these key files:
  - `benchmarks/run_benchmarks.py` — entry point that generates `benchmark_results.md`
  - `benchmarks/bench_import.py` — import time benchmarks
  - `benchmarks/bench_read.py` — file read benchmarks using mock_open
  - `benchmarks/profile_read.py` — phase-level profiler generating `profile_report.md`
  - `benchmarks/README.md` — comprehensive English-language documentation of the suite
  - `benchmarks/benchmark_results.md` — latest benchmark numbers
- Key performance characteristics (from benchmark_results.md):
  - Top-level `import inewave` takes ~0.36s (partially warm cache)
  - Sub-package imports (`inewave.nwlistop`) take ~4.6ms
  - Read times: Earmf ~73ms, Cmarg ~210ms, Pmo ~644ms
  - Aggregation `.valores()` is ~0.1ms on mock data but has O(n^2) scaling on real files
- The lazy import mechanism uses `_LAZY_IMPORTS` dict in each subpackage's `__init__.py`.
- All documentation must be in Brazilian Portuguese.

## Specification

### Requirements

1. Create a new file `docs/source/geral/desempenho.rst` containing the performance guide, entirely in Brazilian Portuguese.
2. The page must cover these topics in order:
   - **Visao Geral de Desempenho**: Brief summary of what affects performance (import time, read time, aggregation time).
   - **Tempos de Importacao**: Explain lazy import mechanism and its impact. Describe why the first `import inewave` is slow (~0.36s) and subsequent sub-package imports are fast (~5ms). Provide tip to import specific subpackages directly.
   - **Tempos de Leitura**: Present representative read times for different file types (non-patamar ~70ms, patamar ~210ms, SectionFile ~644ms). Explain what drives the differences (number of patamar levels, section complexity).
   - **Otimizacao para Processamento em Lote**: Tips for users who read many files: import once, use direct subpackage imports, consider parallel processing with `multiprocessing` or `concurrent.futures`.
   - **Suite de Benchmarks**: Explain how to run `python benchmarks/run_benchmarks.py` and `python benchmarks/profile_read.py`, and how to interpret the output tables.
   - **Limitacoes Conhecidas**: Document the O(n^2) `__monta_tabela` scaling issue, Python-only memory measurements, and mock-data limitations.
3. Include a summary table of representative benchmark numbers using RST table syntax.
4. Include at least one `.. code-block:: bash` showing how to run benchmarks.
5. Include at least one `.. code-block:: python` showing optimized import pattern.
6. Use `.. warning::` for the O(n^2) scaling caveat.
7. Do NOT include raw benchmark numbers that change per-machine — present them as "approximate" with the hardware caveat.
8. Do NOT modify `docs/source/index.rst` — that is handled by ticket-012.
9. Do NOT modify any files in `benchmarks/`.

### Inputs/Props

- `benchmarks/README.md` — source material for benchmark suite description (in English, must be translated).
- `benchmarks/benchmark_results.md` — source for representative numbers.
- `inewave/newave/__init__.py` — lazy import pattern reference.

### Outputs/Behavior

- A single new file `docs/source/geral/desempenho.rst` that renders correctly with `sphinx-build`.
- The page uses the RST label `.. _desempenho:` at the top for cross-referencing.
- All text content is in Brazilian Portuguese.

### Error Handling

- Not applicable — this is static content.

## Acceptance Criteria

- [ ] Given the file `docs/source/geral/desempenho.rst` exists, when inspecting its content, then it contains the RST label `.. _desempenho:` on line 1
- [ ] Given the file `docs/source/geral/desempenho.rst` exists, when inspecting its structure, then it contains section headings for all 6 required topics (Visao Geral, Tempos de Importacao, Tempos de Leitura, Otimizacao para Processamento em Lote, Suite de Benchmarks, Limitacoes Conhecidas)
- [ ] Given the file `docs/source/geral/desempenho.rst` exists, when inspecting its content, then it contains an RST table with at least 4 rows of representative benchmark data
- [ ] Given the file `docs/source/geral/desempenho.rst` exists, when inspecting its content, then it contains a `.. warning::` admonition about O(n^2) aggregation scaling
- [ ] Given the file `docs/source/geral/desempenho.rst` exists, when inspecting its content, then all prose text is in Brazilian Portuguese

## Implementation Guide

### Suggested Approach

1. Create `docs/source/geral/desempenho.rst`.
2. Start with `.. _desempenho:` label and heading "Guia de Desempenho".
3. Translate and adapt content from `benchmarks/README.md` — do not copy English text.
4. For the benchmark numbers table, use RST list-table or grid-table syntax with columns: Operacao, Tipo de Arquivo, Tempo Aproximado.
5. For the import optimization tip, show:
   ```python
   # Em vez de:
   from inewave.newave import Dger, Pmo, Confhd
   # Importe o subpacote diretamente quando precisar de poucos arquivos:
   from inewave.newave.dger import Dger
   ```
6. For the benchmark run section, show `.. code-block:: bash` with the commands from `benchmarks/README.md`.
7. Present numbers as approximate ("~70ms", "~200ms") with a note that values depend on hardware and Python version.

### Key Files to Modify

- `docs/source/geral/desempenho.rst` (new file)

### Patterns to Follow

- Same RST heading hierarchy as other pages: `=` for title, `-` for sections.
- Use `.. code-block::` directives as in `tutorial.rst`.
- Use `.. warning::` and `.. note::` admonitions as appropriate.

### Pitfalls to Avoid

- Do NOT present benchmark numbers as exact/authoritative — they vary by machine.
- Do NOT add this page to `index.rst` — that is ticket-012's job.
- Do NOT modify benchmark suite files.
- Do NOT translate code, command names, or file paths to Portuguese — only prose.

## Testing Requirements

### Unit Tests

Not applicable — documentation-only ticket.

### Integration Tests

- Run `sphinx-build -b html docs/source docs/build` and verify no new errors from the new file.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-006-migrate-sphinx-theme.md
- **Blocks**: ticket-012-update-index-toctree.md

## Effort Estimate

**Points**: 2
**Confidence**: High
