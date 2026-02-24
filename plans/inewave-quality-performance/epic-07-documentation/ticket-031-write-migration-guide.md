# ticket-031 Write migration guide and update changelog for v1.13.0

## Context

### Background

inewave v1.13.0 is the culmination of a 7-epic quality and performance upgrade plan that migrated the library from cfinterface string-based storage to the StorageType enum, replaced 160+ legacy nwlistop block classes with two composable base classes (`TabelaSerieAnual` and `TabelaSeriePatamarAnual`), added schema versioning with `VERSIONS` dicts and `validate()` integration, enabled strict mypy across all production code, implemented lazy imports for `inewave.nwlistop` and `inewave.newave`, and added round-trip test coverage. The existing `CHANGELOG.md` has entries through v1.12.0 but nothing for v1.13.0. There is no migration guide document anywhere in the repository.

Downstream consumers -- primarily `sintetizador-newave` and other CEPEL ecosystem tools -- need a clear guide explaining what changed, what is deprecated, and how to adopt the new patterns. This ticket also absorbs the scope originally planned for ticket-032 (API documentation updates), because the existing sphinx autodoc RST pages pull from class docstrings which are already accurate after the earlier epics. The only documentation update needed beyond the migration guide itself is updating the tutorial's `set_version()` example to show the new `read(version=...)` pattern and adding a CHANGELOG entry.

### Relation to Epic

This is the primary deliverable of epic-07 (Documentation). It communicates all user-facing changes from epics 01-06 to downstream consumers.

### Current State

- `CHANGELOG.md` exists at `/home/rogerio/git/inewave/CHANGELOG.md` with entries from v1.12.0 down to v0.0.98. No v1.13.0 entry.
- No `MIGRATION.md` or `docs/source/migration.rst` exists.
- `inewave/__init__.py` declares `__version__ = "1.13.0"`.
- `docs/source/geral/tutorial.rst` mentions `set_version()` as the versioning API (lines 126-131).
- `examples/plot_versionamento.py` uses `Cmargmed.set_version(versao)` (line 39).
- Sphinx configuration at `docs/source/conf.py` uses `sphinx_rtd_theme`, `numpydoc`, and `sphinx_gallery`. Language is `pt_BR`.
- The existing sphinx RST reference pages (e.g., `docs/source/referencia/nwlistop/arquivos/cmarg.rst`) use `.. autoclass:: Cmarg` with `:members:` and auto-generate from docstrings. These do NOT need content changes.
- Deprecated classes `ValoresSerie` and `ValoresSeriePatamar` emit `DeprecationWarning` at import time. They are kept for backward compatibility.

## Specification

### Requirements

1. **Create `MIGRATION.md`** at the repository root (`/home/rogerio/git/inewave/MIGRATION.md`) in Markdown format (not RST). This is a standalone document, not part of the sphinx build. Written in Portuguese (matching the project's language convention in `CHANGELOG.md` and `docs/`).

2. **Update `CHANGELOG.md`** by prepending a v1.13.0 entry at the top of the file, following the existing format (heading `# 1.13.0`, bullet list of changes).

3. **Update the tutorial** (`docs/source/geral/tutorial.rst`) to replace the `set_version()` mention with the `read(version=...)` pattern, and note that `set_version()` still works but the keyword argument is the preferred approach.

4. **Update the versioning example** (`examples/plot_versionamento.py`) to use `Cmargmed.read(path, version=versao)` instead of calling `Cmargmed.set_version(versao)` then `Cmargmed.read(path)` separately.

### MIGRATION.md Content Structure

The migration guide must cover the following sections in order:

1. **Requisitos de dependencias** -- cfinterface >= 1.9.0 requirement, numpy >= 2.2.1, pandas >= 2.2.3, Python >= 3.10
2. **Alteracoes de API sem quebra de compatibilidade** (non-breaking API changes):
   - `read(version="27")` keyword argument for version-aware reading
   - `VERSIONS` dict on handler classes (Cmarg, Cmargmed, AvlCortesfphaNwv, EcoFpha, AvlDesvfphaS)
   - `validate()` method on versioned handlers
   - Lazy imports for `inewave.nwlistop` and `inewave.newave` (no user action needed, just FYI)
3. **Classes descontinuadas (deprecated)** -- `ValoresSerie`, `ValoresSeriePatamar` emit `DeprecationWarning`. Users should not instantiate them directly, but they still work via legacy handler BLOCKS configurations. No removal timeline specified (deferred to a future major version).
4. **Mudancas internas** (internal changes, for advanced users):
   - New base classes: `TabelaSerieAnual`, `TabelaSeriePatamarAnual`, `_ArquivoSerieBase`, `_ArquivoSeriePatamarBase`
   - `StorageType.BINARY` enum replaces string `"BINARY"` in `hidr.py`, `vazoes.py`
   - `IO[Any]` convention on all read/write overrides
   - Strict mypy on all production modules
5. **Desempenho** -- Brief note pointing to `benchmarks/benchmark_results.md` and the new benchmark docs (ticket-033). Mention lazy imports reduce `import inewave.nwlistop` from ~300ms to ~5ms.
6. **Testes** -- 1140 tests, round-trip coverage for newave handlers, parallel execution support with `pytest -n auto`

### CHANGELOG.md v1.13.0 Entry Content

Concise bullet list covering:

- Dependencia cfinterface atualizada para >= 1.9.0
- Migracao de `StorageType` string para enum em arquivos binarios
- Nova infraestrutura de blocos `TabelaSerieAnual` e `TabelaSeriePatamarAnual` para NWLISTOP
- Suporte a versionamento de arquivos com `VERSIONS` e `read(version=...)`
- Metodo `validate()` para arquivos versionados
- Imports lazy para `inewave.nwlistop` e `inewave.newave`
- Tipagem estrita (`mypy --strict`) em todos os modulos de producao
- Testes de round-trip para handlers do newave
- Suporte a execucao paralela de testes com `pytest-xdist`
- Classes `ValoresSerie` e `ValoresSeriePatamar` marcadas como deprecated

### Error Handling

Not applicable (documentation-only ticket).

## Acceptance Criteria

- [ ] Given no `MIGRATION.md` exists, when this ticket is completed, then `/home/rogerio/git/inewave/MIGRATION.md` exists and contains all 6 sections listed above
- [ ] Given `CHANGELOG.md` starts with `# 1.12.0`, when this ticket is completed, then the first entry is `# 1.13.0` with at least 8 bullet points covering the changes listed above
- [ ] Given the tutorial mentions `set_version()` at line ~128, when this ticket is completed, then the tutorial paragraph explains `read(version=...)` as the preferred pattern and notes `set_version()` is still supported
- [ ] Given `examples/plot_versionamento.py` line 39 calls `Cmargmed.set_version(versao)`, when this ticket is completed, then the example uses `Cmargmed.read(path, version=versao)` instead
- [ ] Given all documentation is in Portuguese, when this ticket is completed, then `MIGRATION.md` and the CHANGELOG entry are written in Portuguese matching the project's existing tone and conventions

## Implementation Guide

### Suggested Approach

1. Create `MIGRATION.md` at `/home/rogerio/git/inewave/MIGRATION.md`. Use the section structure from the specification above. Write in Portuguese. Reference specific class names and module paths so downstream consumers can search their own code.

2. Prepend the v1.13.0 entry to `CHANGELOG.md`. Follow the exact format of existing entries: `# 1.13.0` heading, then `- ` bullet lines. Keep entries concise (one sentence each).

3. Edit `docs/source/geral/tutorial.rst` around lines 125-131. Replace the paragraph about `set_version` with an explanation of the `version=` keyword argument. Show a code example:

   ```python
   cmarg = Cmarg.read("./nwlistop/cmarg001.out", version="27")
   ```

   Mention that `set_version()` still works for backward compatibility.

4. Edit `examples/plot_versionamento.py` line 39. Replace:
   ```python
   Cmargmed.set_version(versao)
   cmarg_v28 = Cmargmed.read("./nwlistop/cmarg001-med_v28.out")
   ```
   With:
   ```python
   cmarg_v28 = Cmargmed.read("./nwlistop/cmarg001-med_v28.out", version=versao)
   ```

### Key Files to Modify

- **Create**: `/home/rogerio/git/inewave/MIGRATION.md`
- **Edit**: `/home/rogerio/git/inewave/CHANGELOG.md` (prepend v1.13.0 entry)
- **Edit**: `/home/rogerio/git/inewave/docs/source/geral/tutorial.rst` (lines ~125-131)
- **Edit**: `/home/rogerio/git/inewave/examples/plot_versionamento.py` (line ~39)

### Patterns to Follow

- Portuguese language throughout, matching the existing `CHANGELOG.md` tone
- Markdown format for `MIGRATION.md` (not RST) since it lives at repo root alongside `README.md` and `CHANGELOG.md`
- Existing CHANGELOG bullet format: `- Description of change`
- Reference class names with backticks in Markdown: `` `TabelaSerieAnual` ``
- For the tutorial RST, use `.. code-block:: python` for code examples (matching existing tutorial pattern)

### Pitfalls to Avoid

- Do NOT modify sphinx RST reference pages (`docs/source/referencia/`). They auto-generate from docstrings and are already correct.
- Do NOT add `MIGRATION.md` to the sphinx toctree. It is a standalone repo-root document.
- Do NOT specify a deprecation removal timeline for `ValoresSerie` / `ValoresSeriePatamar`. The learnings explicitly state deletion is deferred to a future major version.
- Do NOT mention the cfinterface NaT bug (`_is_null()`) in user-facing documentation. It is an internal implementation detail not yet upstreamed.
- The `read(version=...)` kwarg requires the version string to match VERSIONS keys exactly (e.g., `"27"`, not `"v27"` or `27`). Document this.
- Keep the MIGRATION.md focused on what downstream consumers need to DO, not on internal refactoring details they cannot observe.

## Testing Requirements

### Unit Tests

Not applicable (documentation-only).

### Integration Tests

Not applicable (documentation-only).

### Manual Verification

- Read `MIGRATION.md` and verify it covers all 6 sections with accurate information
- Read `CHANGELOG.md` and verify the v1.13.0 entry is well-formed and matches existing format
- Read the updated tutorial section and verify the code example is syntactically correct
- Read the updated versioning example and verify it uses the new API

## Dependencies

- **Blocked By**: None (all epics 01-06 are completed)
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High
