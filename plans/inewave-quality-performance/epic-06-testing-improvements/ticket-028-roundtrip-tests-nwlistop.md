# ticket-028 Add round-trip tests for nwlistop file handlers

## Context

### Background

The nwlistop module contains 171 file handler classes (in `inewave/nwlistop/*.py`) and 172 corresponding test files (in `tests/nwlistop/`). Currently, **zero** of the 172 nwlistop handler test files have file-level round-trip tests. The only round-trip coverage exists at the block level in `tests/nwlistop/test_tabela_serie_anual.py` and `tests/nwlistop/test_tabela_serie_patamar_anual.py`, which test the `TabelaSerieAnual` and `TabelaSeriePatamarAnual` base block classes directly.

After the TabularSection migration (Epic 02), all nwlistop handlers inherit write capability from either `_ArquivoSerieBase` (via `TabelaSerieAnual`) or `_ArquivoSeriePatamarBase` (via `TabelaSeriePatamarAnual`). Both base classes delegate to `TabularParser.format_rows()` for write. The block-level round-trip tests confirm that `TabelaSerieAnual.write()` round-trips correctly, but there is no file-level coverage verifying that the full handler's `read() -> write() -> read()` cycle preserves data integrity (including the header block, concatenation of multiple year blocks, and the `valores` lazy property).

### Relation to Epic

This ticket targets the first goal of Epic 06 for the nwlistop module. It is the largest ticket in the epic due to the volume of files (172 test files). However, the work is highly repetitive -- all nwlistop handlers follow one of three patterns, so the implementation is a batch mechanical task.

### Current State

The nwlistop test files follow a uniform 3-test pattern:

```python
def test_atributos_encontrados_<name>():   # Read + assert values
def test_atributos_nao_encontrados_<name>():  # Read empty + assert None
def test_eq_<name>():                      # Read twice + assert equal
```

Each test file imports a `Mock*` list from `tests/mocks/arquivos/<name>.py` and uses the `mock_open` / `builtins.open` patch pattern.

**Handler architecture**: All nwlistop handlers fall into these categories:

1. **Series-only handlers** (~130 files): Extend `_ArquivoSerieBase` (via `ArquivoREE`, `ArquivoSubmercado`, `ArquivoSIN`, `ArquivoUsina`, etc.). Have a `valores` property returning `Optional[pd.DataFrame]` with columns `["data", "serie", "valor"]`.

2. **Patamar-aware handlers** (~30 files): Extend `_ArquivoSeriePatamarBase` (via corresponding archive classes). Have a `valores` property returning `Optional[pd.DataFrame]` with columns `["data", "patamar", "serie", "valor"]`.

3. **MEDIAS CSV handlers** (9 files): `mediasmerc.py`, `mediasree.py`, etc. These use `pd.read_csv()` and read from real files in `tests/_arquivos/`. They are SectionFile-based, not BlockFile-based.

4. **Special handlers** (4 files): `gtert.py` (excluded from migration), `nwlistopdat.py`, `intercambio.py`, `form_rhq.py`, `form_rhv.py`.

5. **Versioned handlers** (4 files): `cmarg.py`, `cmargmed.py`, `pivarm.py`, `pivarmincr.py` -- have `VERSIONS` dictionaries.

## Specification

### Requirements

1. Add `test_leitura_escrita_<name>` round-trip tests to all nwlistop handler test files where the handler uses mock_open-based testing (i.e., NOT the 9 MEDIAS CSV files that read from real files).
2. For MEDIAS CSV handlers, skip round-trip tests with a comment explaining that they use `pd.read_csv()` and SectionFile-based architecture with no write path.
3. For versioned handlers (`cmarg`, `cmargmed`, `pivarm`, `pivarmincr`), add round-trip tests for their default (latest) version.
4. The round-trip test must use the same mock_open pattern established in `tests/newave/test_adterm.py`.
5. All nwlistop tests use `ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"` as the dummy file path.

### Inputs/Props

- Each test uses the existing `Mock*` list from `tests/mocks/arquivos/<name>.py`.
- The handler class is imported from `inewave.nwlistop.<name>`.
- The `mock_open` utility is imported from `tests/mocks/mock_open`.

### Outputs/Behavior

- Each round-trip test asserts `n1 == n2` where `n1` is the original read and `n2` is re-read from written output.
- The `__eq__` method is inherited from `BlockFile` and already tested by existing `test_eq_*` tests.

### Error Handling

- If write output is empty (no blocks written), the re-read will produce an object with `valores == None`. The `__eq__` comparison will then fail, exposing the bug.
- If a handler's `write()` method is not implemented or produces corrupted output, the round-trip test will fail with a clear assertion.

## Acceptance Criteria

- [ ] Given a series-only nwlistop handler (e.g., `Earmf`), when `test_leitura_escrita_earmf()` is added using mock_open, then read -> write -> read produces `n1 == n2`
- [ ] Given a patamar-aware nwlistop handler (e.g., `Ghidr`), when `test_leitura_escrita_ghidr()` is added using mock_open, then read -> write -> read produces `n1 == n2`
- [ ] Given a versioned handler (e.g., `Cmarg`), when `test_leitura_escrita_cmarg()` is added using the default version, then round-trip passes
- [ ] Given a MEDIAS CSV handler (e.g., `Mediasree`), when no round-trip test is added, then a `# NOTE: MEDIAS CSV file, SectionFile with pd.read_csv, no write path` comment is present
- [ ] Given all new round-trip tests are added, when `pytest tests/nwlistop/ -v` is run, then all tests pass with zero failures
- [ ] Given the full test suite, when `pytest tests/ -v` is run, then the baseline of 1134+ tests (after ticket-027) is maintained plus the new nwlistop round-trip tests (expected ~163 new tests: 172 files minus 9 MEDIAS)

## Implementation Guide

### Suggested Approach

**This is a batch mechanical task.** The approach is to write a single round-trip test template and apply it to all ~163 non-MEDIAS test files.

1. **Create a helper script** (optional, disposable) or use editor macros to generate the round-trip test function for each file. The template for ALL nwlistop files is identical:

```python
def test_leitura_escrita_<name>():
    m_leitura: MagicMock = mock_open(read_data="".join(Mock<Name>))
    with patch("builtins.open", m_leitura):
        n1 = <Handler>.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        n1.write(ARQ_TESTE)
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        n2 = <Handler>.read(ARQ_TESTE)
        assert n1 == n2
```

2. **For each test file**, determine:
   - The handler class name (from the import at the top of the test file, e.g., `from inewave.nwlistop.earmf import Earmf`)
   - The mock variable name (from the import, e.g., `from tests.mocks.arquivos.earmf import MockEarmf`)
   - Substitute into the template

3. **For versioned handlers** (`cmarg`, `cmargmed`, `pivarm`, `pivarmincr`): Use the default mock data (the one without a version suffix) and do NOT pass `version=` to `read()`, so it uses the default/latest version.

4. **For MEDIAS CSV files** (9 files: `test_mediasmerc.py`, `test_mediasree.py`, `test_mediasrep.py`, `test_mediasrhq.py`, `test_mediasrhv.py`, `test_mediassin.py`, `test_mediasusie.py`, `test_mediasusih.py`, `test_mediasusit.py`): Add a comment at the end of each file: `# NOTE: MEDIAS CSV file, SectionFile with pd.read_csv, no write path`

5. **Batch the work**: Process files alphabetically in groups of ~30. After each group, run `pytest tests/nwlistop/ -x` to catch failures early.

6. **Run the full test suite** at the end to confirm no regressions.

### Key Files to Modify

All 172 files in `tests/nwlistop/` excluding:

- `tests/nwlistop/__init__.py` -- package init, no changes
- `tests/nwlistop/test_tabela_serie_anual.py` -- already has block-level round-trip
- `tests/nwlistop/test_tabela_serie_patamar_anual.py` -- already has block-level round-trip
- `tests/nwlistop/test_version_validate.py` -- validation tests, not a handler test

That leaves approximately **168 test files** to modify:

- ~159 files: add `test_leitura_escrita_*` function
- ~9 MEDIAS files: add skip comment only

### Patterns to Follow

- Follow the exact round-trip pattern from `tests/newave/test_adterm.py` lines 57-72.
- The nwlistop tests all use `ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"` (not actual data files). The mock data is injected via `mock_open`.
- Test function naming: `test_leitura_escrita_{handler_name_lowercase}`.
- The handler's `__eq__` is inherited from `BlockFile.__eq__` which compares block lists.

### Pitfalls to Avoid

- **Do NOT add round-trip tests for MEDIAS CSV files** -- they use `pd.read_csv()` via SectionFile and do not have a write path compatible with the mock_open pattern.
- **Check mock variable names carefully** -- some mock files use `MockCmarg`, `MockCmarg27`, `MockCmargmed`, etc. Use the FIRST/default mock (the one used by `test_atributos_encontrados_*`) for the round-trip test.
- **Some nwlistop handlers emit DeprecationWarning** (e.g., `Vturuh.__init__`). Wrap those round-trip tests with `warnings.catch_warnings()` / `warnings.simplefilter("ignore", DeprecationWarning)` if the existing test file already does so.
- **The comment `# Nao deve ter teste de diferenca`** at the end of many nwlistop test files means "should not have an inequality test" (because the `valores` property is a lazy property). This does NOT mean round-trip should be skipped.
- **Do NOT change existing tests** -- only append new test functions and comments.
- **Mock data files can be very large** (e.g., `tests/mocks/arquivos/earmf.py` is 260KB). The `"".join(MockEarmf)` call in the test handles this correctly -- the mock_open utility converts it to a StringIO internally.

## Testing Requirements

### Unit Tests

Each new `test_leitura_escrita_*` function IS a unit test. ~159 new test functions total.

### Integration Tests

Not applicable -- this ticket adds tests, not production code.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: None (all prior epics are completed; ticket-027 is independent)
- **Blocks**: None

## Effort Estimate

**Points**: 5
**Confidence**: High
