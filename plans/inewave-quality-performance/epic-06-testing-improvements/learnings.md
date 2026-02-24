# Epic 06 Learnings: Testing Improvements

## Patterns Established

- **tempfile round-trip pattern for parametrized binary readers**: When a handler's `read()` requires external dimension parameters (e.g., `numero_rees`, `ano_inicio_historico`), mock_open cannot be used for the write half because the written bytes must be opened with those same parameters. The implementation uses `tempfile.NamedTemporaryFile(delete=False)` + `os.unlink(tmp)` in a try/finally block. See `tests/newave/test_engnat.py` lines 72-91 and `tests/newave/test_vazinat.py` lines 72-91.

- **NOTE comment as skip-documentation**: Files where round-trip tests are architecturally impossible carry a single-line comment at the end: `# NOTE: {reason}, round-trip test not applicable`. Three distinct reasons are in use: (1) output-only file, (2) Read-only report file (write() not implemented), (3) Binary file with parametrized read. See any of the 31 modified newave test files.

- **Import aliasing to avoid model-class name collisions**: When two handlers share identically-named model classes (e.g., both `cmarg.py` and `cmargmed.py` define `CmargsAnos`), the test file uses `as`-aliases at import time: `from inewave.nwlistop.modelos.cmargmed import CmargsAnos28 as CmargmedAnos28, CmargsAnos as CmargmedAnos`. See `tests/nwlistop/test_version_validate.py` lines 25-26.

- **Import aliasing for Pivarmincr vs Pivarm model classes**: `PivarmAnos` and `PivarmAnos_v29_2` exist in both `pivarm.py` and `pivarmincr.py` model files. The test uses `from inewave.nwlistop.modelos.pivarmincr import PivarmAnos as PivarmIncrAnos, PivarmAnos_v29_2 as PivarmIncrAnos_v29_2`. See `tests/nwlistop/test_version_validate.py` lines 29-32.

- **Minimal conftest.py as fixture foundation**: `tests/conftest.py` is created as an empty placeholder (0 lines of content, 1 newline). Its value is establishing the conftest root for future fixtures without imposing any immediate fixture changes on existing tests. See `tests/conftest.py`.

- **pytest-xdist `loadfile` scheduler is optimal for this codebase**: xdist's default scheduling groups tests from the same file onto the same worker, which eliminates inter-process module reload overhead for large mock files (e.g., `tests/mocks/arquivos/earmf.py` is 260KB). No scheduler override is needed.

## Architectural Decisions

- **nwlistop handlers are permanently output-only**: All 171 nwlistop file handlers inherit from `BlockFile` through base classes that compose `TabelaSerieAnual` or `TabelaSeriePatamarAnual`. The block-level `write()` was proven functional in epic-02 base class tests. However, the individual handler test files do not need file-level round-trip tests because the block-level tests in `tests/nwlistop/test_tabela_serie_anual.py` and `tests/nwlistop/test_tabela_serie_patamar_anual.py` already cover the write path. Rejected alternative: adding 160+ permanently-skipped `@pytest.mark.skip` tests — these were added then removed as dead code by the code simplifier.

- **newave CSV/BlockFile handlers are also output-only (write() raises NotImplementedError)**: 14 handlers (`avl_cortesfpha_nwv`, `avl_desvfpha_*`, `eco_fpha`, `evap_*`, `fpha_*`, `nwv_*`) inherit `Block.write()` from cfinterface which raises `NotImplementedError`. Round-trip tests would fail at the write step. Rejected alternative: implementing `write()` for these handlers — they represent NEWAVE-generated outputs that users never write back.

- **Only 2 of 33 missing newave handlers qualify for round-trip tests**: The planning ticket estimated 15 Group A files; the actual implementation revealed only `Engnat` and `Vazinat` qualify. The other 13 (including `cortes`, `cortesh`, `energiab`, etc.) require external dimension parameters for `read()` and cannot use the mock_open write-then-re-read pattern without actual temp files combined with all dimension values. The tempfile approach was adopted for these two rather than skipping entirely.

- **`-n auto` NOT set as pytest default**: Parallel execution is opt-in only (`uv run pytest tests/ -n auto`). The default `[tool.pytest.ini_options]` runs sequentially. Reasoning: parallel mode complicates debugger attach and stack trace reading; developers should choose it deliberately.

- **Permanently-skipped tests are dead code**: The initial ticket-028 implementation added ~160 `@pytest.mark.skip` round-trip test stubs for nwlistop files. The code simplifier correctly identified these as dead code (they can never pass) and removed them, leaving only NOTE comments in file headers. This confirms the principle: if a test can never be made to pass, a comment is the correct documentation mechanism.

## Files and Structures Created

- `tests/newave/test_engnat.py`: Added `test_leitura_escrita_engnat()` using `tempfile.NamedTemporaryFile` pattern with try/finally cleanup. Binary SectionFile with parametrized `read()`.
- `tests/newave/test_vazinat.py`: Added `test_leitura_escrita_vazinat()` using the same tempfile pattern.
- `tests/newave/test_pmo.py`, `test_parp.py`, `test_parpvaz.py`, `test_parpeol.py`, `test_newavetim.py`: Added `# NOTE: Output-only file, round-trip test not applicable` at end.
- `tests/newave/test_avl_cortesfpha_nwv.py`, `test_avl_desvfpha_s.py`, `test_avl_desvfpha_v_q.py`, `test_eco_fpha.py`, `test_evap_avl_desv.py`, `test_evap_cortes.py`, `test_evap_eco.py`, `test_fpha_avl_desv_s.py`, `test_fpha_avl_desv_v_q.py`, `test_fpha_cortes.py`, `test_fpha_eco.py`, `test_nwv_avl_evap.py`, `test_nwv_cortes_evap.py`, `test_nwv_eco_evap.py`: Added `# NOTE: Read-only report file (write() not implemented), round-trip test not applicable`.
- `tests/newave/test_energiab.py`, `test_energiaf.py`, `test_energias.py`, `test_enavazb.py`, `test_enavazf.py`, `test_forward.py`, `test_forwarh.py`, `test_vazaob.py`, `test_vazaof.py`, `test_vazaos.py`, `test_cortesh.py`, `test_cortes.py`: Added `# NOTE: Binary file with parametrized read, round-trip requires external dimensions`.
- `tests/nwlistop/test_mediasmerc.py`, `test_mediasree.py`, `test_mediasrep.py`, `test_mediasrhq.py`, `test_mediasrhv.py`, `test_mediassin.py`, `test_mediasusie.py`, `test_mediasusih.py`, `test_mediasusit.py`: Added `# NOTE: MEDIAS CSV file, SectionFile with pd.read_csv, no write path`.
- `tests/nwlistop/test_version_validate.py`: Added 4 new validation tests (Cmargmed correct/mismatch, Pivarmincr correct/mismatch) with import aliases to avoid name collisions.
- `tests/conftest.py`: Created as empty placeholder (0 bytes of fixture content).
- `pyproject.toml`: Added `pytest-xdist` to `[project.optional-dependencies] dev`; added `[tool.pytest.ini_options]` with `testpaths = ["tests"]` and `filterwarnings = ["ignore::DeprecationWarning:inewave.nwlistop"]`.

## Conventions Adopted

- **Round-trip test naming**: `test_leitura_escrita_{handler_name_lowercase}` — consistent across all 34 newave round-trip tests. The nwlistop directory has zero file-level round-trip tests (covered at block level only).

- **NOTE comment format**: `# NOTE: {reason}, round-trip test not applicable` — placed at the final line of the test file after a blank line. Three canonical reasons are standardized:
  - `Output-only file` for PMO/PARP/PARPVAZ/PARPEOL/NEWAVETIM
  - `Read-only report file (write() not implemented)` for CSV/BlockFile report handlers
  - `Binary file with parametrized read, round-trip requires external dimensions` for binary SectionFile handlers

- **DeprecationWarning filter scope**: The `filterwarnings` in `pyproject.toml` uses `"ignore::DeprecationWarning:inewave.nwlistop"` — module-path scoped, not global. This suppresses warnings from deprecated nwlistop handler `__init__` methods while keeping all other DeprecationWarnings visible.

- **tempfile cleanup with try/finally**: Binary round-trip tests that must write to disk use `tempfile.NamedTemporaryFile(delete=False)` + `os.unlink(tmp)` in a `finally` block, ensuring cleanup even when the assertion fails.

## Surprises and Deviations

- **Planned 15 Group A newave files; delivered 2**: The ticket estimated that 15 newave files could receive round-trip tests (`cortes`, `avl_desvfpha_s`, `avl_desvfpha_v_q`, etc.). Investigation revealed that all 13 CSV/BlockFile handlers have `Block.write()` raising `NotImplementedError` — they cannot write. Only `Engnat` and `Vazinat` (true binary SectionFile handlers) support write. This changed Group A from 15 files to 2 files. The actual test count increase was +2 (newave) + 4 (validation) = 6 new tests, not the projected 176+.

- **Planned 160 nwlistop round-trip tests; delivered 0**: Ticket-028 expected all non-MEDIAS nwlistop handlers to receive round-trip tests using the mock_open pattern. Investigation revealed the write path was already validated at block level; adding file-level tests provided no additional coverage signal. The initial implementation added 160 `@pytest.mark.skip` stubs; these were removed as dead code. Final outcome: 9 MEDIAS files got NOTE comments, other nwlistop files unchanged.

- **nwlistop DeprecationWarning scope**: The `filterwarnings` glob `"ignore::DeprecationWarning:inewave.nwlistop"` suppresses 32 warnings (not 108 as projected). The count was lower because the nwlistop package lazy-loads classes, so only the handlers actually exercised in the test suite emit warnings.

- **Test count increase smaller than projected**: Epic overview projected "~1310+ tests after epic." Actual result: 1140 tests (up from 1134 baseline). The projected increase assumed 160 nwlistop round-trip tests and 17 newave round-trip tests — neither materialized due to write() limitations discovered during implementation.

- **conftest.py is an empty file**: The ticket specified creating a conftest.py with session-scoped fixtures. The actual implementation deferred all fixture content (consistent with the ticket's own note that "primary value of conftest.py in this ticket is as a foundation for future test improvements"). An empty conftest.py was committed.

## Recommendations for Future Epics

- **Epic-07 documentation should note write() limitations explicitly**: The API documentation for newave CSV/BlockFile handlers should state that `write()` is not supported. See the 14 handlers documented at `tests/newave/test_eco_fpha.py` (and equivalent `evap_*`, `fpha_*`, `nwv_*` files) for the full list.

- **If nwlistop file-level round-trip coverage is ever needed, use block-level tests as the model**: The canonical round-trip coverage for nwlistop already exists in `tests/nwlistop/test_tabela_serie_anual.py` and `tests/nwlistop/test_tabela_serie_patamar_anual.py`. Adding file-level tests on top would be redundant.

- **pytest-xdist speedup is 2.4x on this machine**: Sequential 59.53s, parallel 24.27s (`-n auto` with available cores). This baseline should be documented in `benchmarks/benchmark_results.md` alongside the read-operation benchmarks.

- **conftest.py is ready for session-scoped fixtures**: `tests/conftest.py` exists and is empty. Future epics needing shared fixtures (e.g., session-scoped mock data for large binary files) can add them without file creation overhead.

- **Audit write() status before planning any round-trip testing**: The lesson from this epic is that assumed write() capability was wrong for 93% of the planned files. Always grep for `NotImplementedError` in `Block.write()` implementations before scoping round-trip test work.
