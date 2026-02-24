# ticket-027 Add round-trip tests for newave file handlers

## Context

### Background

The inewave test suite currently has 1134 tests across `tests/newave/` (64 files, 499 test functions) and `tests/nwlistop/` (172 files, 565 test functions). Round-trip tests (read -> write -> read -> compare) are the strongest correctness guarantee for file I/O handlers, because they validate both the read and write paths in a single assertion. After the TabularSection migration (epics 01-02), the type safety improvements (epic 05), and the version catalog audit (epic 03), this is the right time to close the round-trip coverage gap.

### Relation to Epic

This ticket targets the first goal of Epic 06: "Add round-trip tests (read -> write -> read) for all file types." It covers specifically the `tests/newave/` directory. Ticket-028 covers the `tests/nwlistop/` directory separately due to the different handler architecture and larger volume.

### Current State

**31 of 64** newave test files already have a `test_leitura_escrita_*` round-trip test. The following **33 test files** lack round-trip tests:

**Text-based BlockFile handlers (output-only files -- no round-trip expected):**

- `test_pmo.py` -- `Pmo` reads `pmo.dat`, a complex output summary with 22 block types. This is a read-only output file from NEWAVE; `write()` is inherited from `BlockFile` but not meaningfully exercised by users.
- `test_parp.py` -- 9 block types, output-only
- `test_parpvaz.py` -- 9 block types, output-only
- `test_parpeol.py` -- 6 block types, output-only
- `test_newavetim.py` -- 2 block types, timing output

**CSV/BlockFile handlers (newave-internal CSV-format files):**

- `test_avl_cortesfpha_nwv.py` -- deprecated, replaced by `fpha_cortes.py`
- `test_avl_desvfpha_s.py`, `test_avl_desvfpha_v_q.py`
- `test_eco_fpha.py`
- `test_evap_avl_desv.py`, `test_evap_cortes.py`, `test_evap_eco.py`
- `test_fpha_avl_desv_s.py`, `test_fpha_avl_desv_v_q.py`, `test_fpha_cortes.py`, `test_fpha_eco.py`
- `test_nwv_avl_evap.py`, `test_nwv_cortes_evap.py`, `test_nwv_eco_evap.py`

**Binary SectionFile handlers (parametrized read with external dimensions):**

- `test_energiab.py`, `test_energiaf.py`, `test_energias.py`
- `test_enavazb.py`, `test_enavazf.py`
- `test_forward.py`, `test_forwarh.py`
- `test_vazaob.py`, `test_vazaof.py`, `test_vazaos.py`
- `test_cortesh.py` -- binary with internal version field
- `test_cortes.py` -- text, but reads `cortes_ree.dat` / `cortes_hib.dat`

**Text SectionFile/BlockFile handlers (should support round-trip):**

- `test_engnat.py` -- text SectionFile
- `test_vazinat.py` -- text SectionFile

The existing round-trip pattern in 31 files follows this template (from `test_adterm.py`):

```python
def test_leitura_escrita_adterm():
    m_leitura: MagicMock = mock_open(read_data="".join(MockAdterm))
    with patch("builtins.open", m_leitura):
        ad1 = Adterm.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ad1.write(ARQ_TESTE)
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ad2 = Adterm.read(ARQ_TESTE)
        assert ad1 == ad2
```

For binary files like `hidr.py`, the pattern uses `b"".join(linhas_escritas)` instead of `"".join(linhas_escritas)`.

## Specification

### Requirements

1. Add `test_leitura_escrita_*` round-trip tests to all text-based newave handler test files that currently lack them and support meaningful write operations.
2. Add binary round-trip tests to binary SectionFile handlers where the read API does not require external dimensions (only `hidr.py` and `vazoes.py` already have round-trip tests; no new binary files qualify without external dimensions).
3. Skip round-trip tests for files that are output-only (`pmo.py`, `parp.py`, `parpvaz.py`, `parpeol.py`, `newavetim.py`) -- instead, add a comment documenting why round-trip is not applicable.
4. Skip round-trip tests for binary files requiring external parametrized dimensions (`energiab`, `energiaf`, `energias`, `enavazb`, `enavazf`, `forward`, `forwarh`, `vazaob`, `vazaof`, `vazaos`) -- these files require `numero_forwards`, `numero_rees`, etc. parameters that come from other NEWAVE files. Add a comment documenting this.
5. Add round-trip tests for the CSV/BlockFile handlers where write is inherited from `BlockFile` and mock data exists.

### Inputs/Props

- Each round-trip test takes the existing `Mock*` data from `tests/mocks/arquivos/*.py` as input.
- Text handlers: `"".join(Mock*)`
- Binary handlers: `b"".join(Mock*)` or read from actual binary files in `tests/mocks/arquivos/`.

### Outputs/Behavior

- Each round-trip test asserts `ad1 == ad2` where `ad1` is the original read and `ad2` is re-read from written output.
- The `__eq__` method on all handler classes is already implemented (tested by existing `test_eq_*` tests).

### Error Handling

- If `write()` fails or produces empty output, the round-trip test will fail with a clear assertion error.
- If `__eq__` comparison fails due to floating-point precision issues in write output, the test exposes a real bug in the write path that must be investigated (not suppressed).

## Acceptance Criteria

- [ ] Given a text-based newave handler with a `Mock*` data file and no parametrized read API, when a round-trip test is added, then `read -> write -> read` produces an object equal to the original (`ad1 == ad2`)
- [ ] Given a CSV/BlockFile handler (avl*, eco*, evap*, fpha*, nwv\*) whose underlying Block.write() raises NotImplementedError, when no round-trip test is added, then a `# NOTE: Read-only report file (write() not implemented), round-trip test not applicable` comment is present
- [ ] Given an output-only handler (pmo, parp, parpvaz, parpeol, newavetim), when no round-trip test is added, then a `# NOTE: Output-only file, round-trip not applicable` comment is present in the test file
- [ ] Given a binary handler requiring external dimensions (energiab, forward, etc.), when no round-trip test is added, then a `# NOTE: Binary file with parametrized read, round-trip requires external dimensions` comment is present
- [ ] Given all new round-trip tests are added, when `pytest tests/newave/ -v` is run, then all tests pass with zero failures
- [ ] Given the full test suite, when `pytest tests/ -v` is run, then the baseline of 1134 tests is maintained plus 2 new round-trip tests (Engnat, Vazinat) for a total of 1136

## Implementation Guide

### Suggested Approach

1. **Categorize the 33 missing files** into three groups:
   - **Group A: Add round-trip test** -- text-based handlers with mock data and standard read API (~15 files: `engnat`, `vazinat`, `cortes`, `avl_desvfpha_s`, `avl_desvfpha_v_q`, `avl_cortesfpha_nwv`, `eco_fpha`, `evap_avl_desv`, `evap_cortes`, `evap_eco`, `fpha_avl_desv_s`, `fpha_avl_desv_v_q`, `fpha_cortes`, `fpha_eco`, `nwv_avl_evap`, `nwv_cortes_evap`, `nwv_eco_evap`)
   - **Group B: Skip with comment** -- output-only files (5 files: `pmo`, `parp`, `parpvaz`, `parpeol`, `newavetim`)
   - **Group C: Skip with comment** -- binary parametrized files (13 files: `energiab`, `energiaf`, `energias`, `enavazb`, `enavazf`, `forward`, `forwarh`, `vazaob`, `vazaof`, `vazaos`, `cortesh`, `cortes`)

2. **For Group A**, add a `test_leitura_escrita_*` function following the exact pattern in `tests/newave/test_adterm.py`:
   - Import the Mock data and handler class (already imported in each test file)
   - Use `mock_open(read_data="".join(Mock*))` for initial read
   - Use `mock_open(read_data="")` for write, then extract written lines from `m_escrita.mock_calls`
   - Use `mock_open(read_data="".join(linhas_escritas))` for re-read
   - Assert `ad1 == ad2`

3. **For the deprecated `avl_cortesfpha_nwv`**, use `warnings.catch_warnings()` and `warnings.simplefilter("ignore", DeprecationWarning)` around the read/write calls, following the pattern in `tests/nwlistop/test_version_validate.py`.

4. **For Groups B and C**, add a single-line comment at the end of each test file explaining why no round-trip test exists.

5. **Run the full test suite** to confirm no regressions.

### Key Files to Modify

- `tests/newave/test_engnat.py` -- add `test_leitura_escrita_engnat()`
- `tests/newave/test_vazinat.py` -- add `test_leitura_escrita_vazinat()`
- `tests/newave/test_avl_cortesfpha_nwv.py` -- add round-trip with deprecation warning suppression
- `tests/newave/test_avl_desvfpha_s.py` -- add round-trip
- `tests/newave/test_avl_desvfpha_v_q.py` -- add round-trip
- `tests/newave/test_eco_fpha.py` -- add round-trip
- `tests/newave/test_evap_avl_desv.py` -- add round-trip
- `tests/newave/test_evap_cortes.py` -- add round-trip
- `tests/newave/test_evap_eco.py` -- add round-trip
- `tests/newave/test_fpha_avl_desv_s.py` -- add round-trip
- `tests/newave/test_fpha_avl_desv_v_q.py` -- add round-trip
- `tests/newave/test_fpha_cortes.py` -- add round-trip
- `tests/newave/test_fpha_eco.py` -- add round-trip
- `tests/newave/test_nwv_avl_evap.py` -- add round-trip
- `tests/newave/test_nwv_cortes_evap.py` -- add round-trip
- `tests/newave/test_nwv_eco_evap.py` -- add round-trip
- `tests/newave/test_pmo.py` -- add skip comment
- `tests/newave/test_parp.py` -- add skip comment
- `tests/newave/test_parpvaz.py` -- add skip comment
- `tests/newave/test_parpeol.py` -- add skip comment
- `tests/newave/test_newavetim.py` -- add skip comment
- `tests/newave/test_energiab.py` -- add skip comment
- `tests/newave/test_energiaf.py` -- add skip comment
- `tests/newave/test_energias.py` -- add skip comment
- `tests/newave/test_enavazb.py` -- add skip comment
- `tests/newave/test_enavazf.py` -- add skip comment
- `tests/newave/test_forward.py` -- add skip comment
- `tests/newave/test_forwarh.py` -- add skip comment
- `tests/newave/test_vazaob.py` -- add skip comment
- `tests/newave/test_vazaof.py` -- add skip comment
- `tests/newave/test_vazaos.py` -- add skip comment
- `tests/newave/test_cortesh.py` -- add skip comment
- `tests/newave/test_cortes.py` -- add skip comment

### Patterns to Follow

- Follow the exact round-trip pattern from `tests/newave/test_adterm.py` line 57-72.
- Import convention: `from tests.mocks.mock_open import mock_open` and `from unittest.mock import MagicMock, patch`.
- Test naming: `test_leitura_escrita_{handler_name}` (consistent with existing 31 tests).
- Skip comment format: `# NOTE: {reason}, round-trip test not applicable`

### Pitfalls to Avoid

- Do NOT add round-trip tests for binary files with parametrized `read()` -- the test would need external dimension parameters that come from other NEWAVE files.
- Do NOT suppress floating-point comparison failures -- they indicate real bugs.
- For `avl_cortesfpha_nwv`, do NOT forget the deprecation warning suppression -- the `AvlCortesFpha.__init__` emits `DeprecationWarning`.
- Check that the Mock\* data variable exists in the corresponding mock file before writing the test. Some test files may use different Mock variable names (check imports at the top of each test file).
- The `"".join()` call must match what the test file uses. Some mock files return a single list (e.g., `MockEngnat = [...]`), others return multiple lists for different blocks. Check each mock file's import.

## Testing Requirements

### Unit Tests

Each new `test_leitura_escrita_*` function IS a unit test. No additional testing infrastructure needed.

### Integration Tests

Not applicable -- this ticket adds tests, not production code.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: None (all prior epics are completed)
- **Blocks**: None

## Effort Estimate

**Points**: 3
**Confidence**: High
