# ticket-020 Optimize DataFrame creation in archive base classes

## Context

### Background

All 13 nwlistop archive base classes in `inewave/nwlistop/modelos/arquivos/` share an identical `__monta_tabela()` pattern: iterate over `self.data` blocks, filter by type, and repeatedly call `pd.concat([df, b.data], ignore_index=True)` in a loop. This is O(n^2) in the number of year blocks because each `pd.concat` copies all previous data. A typical NEWAVE output file has 5-30 year blocks, so the quadratic cost is noticeable. The fix is to collect all DataFrames into a list first, then call `pd.concat` once.

Additionally, each block's `_build_dataframe()` method (in `TabelaSerieAnual` and `TabelaSeriePatamarAnual`) calls `formata_df_meses_para_datas_nwlistop()` which pivots the wide-format (12 month columns) into tidy/long format (data, serie, valor). This involves `np.tile`, `np.repeat`, `np.concatenate`, and a final `pd.DataFrame()` constructor. The profiling report from ticket-019 will confirm whether the bottleneck is in the concat loop, in `formata_df_meses_para_datas_nwlistop`, or both.

### Relation to Epic

This ticket addresses the most impactful optimization target in the read path: the DataFrame aggregation in archive base classes. After parsing (which is dominated by cfinterface's `Line.read()` and `FloatField._textual_read()`, both already optimized in cfinterface 1.9.0), DataFrame creation and aggregation are the next most expensive operations. Optimizing these 13 files benefits all ~170 nwlistop handlers that extend them.

### Current State

The 13 archive base classes and their `__monta_tabela()` patterns are:

**Non-patamar (use `TabelaSerieAnual` / `ValoresSerie` isinstance check):**

1. `inewave/nwlistop/modelos/arquivos/arquivoree.py` - `ArquivoREE`
2. `inewave/nwlistop/modelos/arquivos/arquivosin.py` - `ArquivoSIN`
3. `inewave/nwlistop/modelos/arquivos/arquivousina.py` - `ArquivoUsina`
4. `inewave/nwlistop/modelos/arquivos/arquivosubmercado.py` - `ArquivoSubmercado`
5. `inewave/nwlistop/modelos/arquivos/arquivorestricao.py` - `ArquivoRestricao`

**Patamar (use `TabelaSeriePatamarAnual` / `ValoresSeriePatamar` isinstance check):** 6. `inewave/nwlistop/modelos/arquivos/arquivoreepatamar.py` - `ArquivoREEPatamar` 7. `inewave/nwlistop/modelos/arquivos/arquivosinpatamar.py` - `ArquivoSINPatamar` 8. `inewave/nwlistop/modelos/arquivos/arquivousinapatamar.py` - `ArquivoUsinaPatamar` 9. `inewave/nwlistop/modelos/arquivos/arquivosubmercadopatamar.py` - `ArquivoSubmercadoPatamar` 10. `inewave/nwlistop/modelos/arquivos/arquivorestricaopatamar.py` - `ArquivoRestricaoPatamar` 11. `inewave/nwlistop/modelos/arquivos/arquivoparsubmercadopatamar.py` - `ArquivoParSubmercadoPatamar` 12. `inewave/nwlistop/modelos/arquivos/arquivoestacaobombeamentopatamar.py` - `ArquivoEstacaoBombeamentoPatamar`

**Special (uses `ValoresClasseTermicaSeriePatamar` / `TabelaSeriePatamarAnual`):** 13. `inewave/nwlistop/modelos/arquivos/arquivoclassetermicasubmercadopatamar.py` - `ArquivoClasseTermicaSubmercadoPatamar`

The current `__monta_tabela()` in every one of these classes follows this exact pattern:

```python
def __monta_tabela(self) -> pd.DataFrame:
    df = None
    for b in self.data:
        if not isinstance(b, (OldType, NewType)):
            continue
        if b.data is None:
            continue
        elif df is None:
            df = b.data
        else:
            df = pd.concat([df, b.data], ignore_index=True)
    return df
```

Some files have a minor variant where `dados = b.data` is assigned to a local variable first (e.g., `ArquivoREEPatamar`, `ArquivoSubmercado`, `ArquivoRestricao`, `ArquivoRestricaoPatamar`, `ArquivoParSubmercadoPatamar`, `ArquivoEstacaoBombeamentoPatamar`), but the logic is identical.

## Specification

### Requirements

1. Replace the O(n^2) `pd.concat` loop in all 13 `__monta_tabela()` methods with a collect-then-concat pattern: accumulate DataFrames in a list, then call `pd.concat(dfs_list, ignore_index=True)` once at the end. This is O(n).
2. The replacement must preserve:
   - The `isinstance()` dual-type guard (checking both old and new block types)
   - The `None` check on `b.data`
   - The return type (`pd.DataFrame` or `None` when no blocks match)
   - The `ignore_index=True` behavior
3. The lazy caching pattern via `self.__valores` must be preserved unchanged.
4. No changes to the `valores` property, the header-block properties (e.g., `ree`, `submercado`, `usina`, `restricao`, `estacao`, `submercado_de`, `submercado_para`), or any other public API.

### Inputs/Props

Each `__monta_tabela()` receives no arguments; it reads from `self.data` (the list of parsed Block instances managed by cfinterface's `BlockFile`).

### Outputs/Behavior

The return value of `__monta_tabela()` must be identical DataFrame content (same columns, same dtypes, same values, same row order) as the current implementation. The only change is performance: O(n) instead of O(n^2) in the number of year blocks.

### Error Handling

- If no blocks match the isinstance check, return `None` (same as current behavior).
- If all matching blocks have `b.data is None`, return `None`.

## Acceptance Criteria

- [ ] Given any of the 13 archive base classes, when inspecting `__monta_tabela()`, then it uses a list-collect pattern followed by a single `pd.concat()` call (no `pd.concat` inside a loop)
- [ ] Given all 13 files have been modified, when running `pytest tests/ -x -q`, then all 1134 tests pass with no failures
- [ ] Given a handler that reads a multi-year file (e.g., `Earmf` with `MockEarmf` data), when comparing `handler.valores` before and after the change, then the DataFrame content is identical (same shape, same values, same dtypes)
- [ ] Given the optimized code, when `__monta_tabela()` is called on a file with N year blocks, then `pd.concat` is called exactly once (not N-1 times)
- [ ] Given the 13 files, when inspecting each, then the `isinstance()` dual-type guard is preserved unchanged, and the `valores` lazy property is preserved unchanged

## Implementation Guide

### Suggested Approach

For each of the 13 files, replace the `__monta_tabela()` method body with this pattern:

**For non-patamar files (ArquivoREE, ArquivoSIN, ArquivoUsina, ArquivoSubmercado, ArquivoRestricao):**

```python
def __monta_tabela(self) -> pd.DataFrame:
    dfs = [
        b.data
        for b in self.data
        if isinstance(b, (ValoresSerie, TabelaSerieAnual))
        and b.data is not None
    ]
    if not dfs:
        return None
    return pd.concat(dfs, ignore_index=True)
```

**For patamar files (ArquivoREEPatamar, ArquivoSINPatamar, ArquivoUsinaPatamar, ArquivoSubmercadoPatamar, ArquivoRestricaoPatamar, ArquivoParSubmercadoPatamar, ArquivoEstacaoBombeamentoPatamar):**

```python
def __monta_tabela(self) -> pd.DataFrame:
    dfs = [
        b.data
        for b in self.data
        if isinstance(b, (ValoresSeriePatamar, TabelaSeriePatamarAnual))
        and b.data is not None
    ]
    if not dfs:
        return None
    return pd.concat(dfs, ignore_index=True)
```

**For the special class (ArquivoClasseTermicaSubmercadoPatamar):**

```python
def __monta_tabela(self) -> pd.DataFrame:
    dfs = [
        b.data
        for b in self.data
        if isinstance(
            b, (ValoresClasseTermicaSeriePatamar, TabelaSeriePatamarAnual)
        )
        and b.data is not None
    ]
    if not dfs:
        return None
    return pd.concat(dfs, ignore_index=True)
```

Process each file one at a time, preserving all other code (imports, class definition, properties, `__slots__`, `BLOCKS`, `__init__`).

### Key Files to Modify

1. `inewave/nwlistop/modelos/arquivos/arquivoree.py` (lines 27-38)
2. `inewave/nwlistop/modelos/arquivos/arquivosin.py` (lines 26-37)
3. `inewave/nwlistop/modelos/arquivos/arquivousina.py` (lines 27-38)
4. `inewave/nwlistop/modelos/arquivos/arquivosubmercado.py` (lines 29-41)
5. `inewave/nwlistop/modelos/arquivos/arquivorestricao.py` (lines 29-41)
6. `inewave/nwlistop/modelos/arquivos/arquivoreepatamar.py` (lines 29-42)
7. `inewave/nwlistop/modelos/arquivos/arquivosinpatamar.py` (lines 26-38)
8. `inewave/nwlistop/modelos/arquivos/arquivousinapatamar.py` (lines 27-39)
9. `inewave/nwlistop/modelos/arquivos/arquivosubmercadopatamar.py` (lines 27-39)
10. `inewave/nwlistop/modelos/arquivos/arquivorestricaopatamar.py` (lines 29-42)
11. `inewave/nwlistop/modelos/arquivos/arquivoparsubmercadopatamar.py` (lines 29-42)
12. `inewave/nwlistop/modelos/arquivos/arquivoestacaobombeamentopatamar.py` (lines 29-42)
13. `inewave/nwlistop/modelos/arquivos/arquivoclassetermicasubmercadopatamar.py` (lines 30-44)

### Patterns to Follow

- The list comprehension pattern is preferred for conciseness and because it is idiomatic pandas.
- Preserve the exact `isinstance()` type tuple from each file. Do not change which types are checked.
- The return type annotation `-> pd.DataFrame` is already on `__monta_tabela()` in all files. It returns `None` in the empty case, which is consistent with the `Optional[pd.DataFrame]` annotation on the `valores` property.

### Pitfalls to Avoid

- Do NOT remove unused imports. `ValoresSerie` and `ValoresSeriePatamar` are still imported because they appear in the `isinstance()` check (backward compatibility with any data parsed by old block types).
- Do NOT change the `BLOCKS` class attribute or the `__init__` method.
- Do NOT touch the `valores` property or any header-block property.
- Do NOT remove `TypeVar("T")` declarations even if unused; they exist in several files and removing them is a separate cleanup concern.
- In `ArquivoREEPatamar`, `ArquivoSubmercado`, `ArquivoRestricao`, `ArquivoRestricaoPatamar`, `ArquivoParSubmercadoPatamar`, and `ArquivoEstacaoBombeamentoPatamar`, the current code assigns `dados = b.data` to a local variable. The list comprehension eliminates this intermediate variable, which is fine.

## Testing Requirements

### Unit Tests

No new tests needed. The existing 1134 tests cover all 13 archive base classes through their concrete handler tests. Every handler test reads mock data and checks `handler.valores` values, which exercises `__monta_tabela()`.

### Integration Tests

- Run `pytest tests/ -x -q` and verify all 1134 tests pass.
- Spot-check 3 handler tests to confirm DataFrame contents are unchanged:
  - `pytest tests/nwlistop/test_earmf.py -v` (non-patamar REE)
  - `pytest tests/nwlistop/test_cmarg.py -v` (patamar submercado, versioned)
  - `pytest tests/nwlistop/test_gtert.py -v` (special class-termica type)

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-019 (profiling report confirms this optimization target)
- **Blocks**: ticket-022 (benchmark suite needs optimized code as baseline)

## Effort Estimate

**Points**: 2
**Confidence**: High
