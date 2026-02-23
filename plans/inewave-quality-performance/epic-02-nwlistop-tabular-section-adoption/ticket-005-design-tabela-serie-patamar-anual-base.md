# ticket-005 Design and implement TabelaSeriePatamarAnual TabularSection base class

## Context

### Background

The nwlistop module uses `ValoresSeriePatamar` (in `inewave/nwlistop/modelos/blocos/valoresseriepatamar.py`) as the base class for 87 block subclasses that parse year-grouped tabular data with series+patamar rows and monthly columns. This is similar to `ValoresSerie` (ticket-004) but more complex: each data row has a series number (which may be blank for continuation rows within a patamar group) and a patamar identifier.

### Relation to Epic

This is the second foundation ticket. Together with ticket-004, it provides the base classes that ALL ~162 nwlistop model files will be migrated to.

### Current State

`ValoresSeriePatamar` in `/home/rogerio/git/inewave/inewave/nwlistop/modelos/blocos/valoresseriepatamar.py`:

- `BEGIN_PATTERN = "     ANO: "`
- `END_PATTERN = " MEDIA"`
- `HEADER_LINE` and `DATA_LINE` are `Line([])` (overridden by subclasses)
- `read()`: reads year from header, then loops data lines. Tracks `__serie_atual` -- when a data line has `dados[0] is not None`, it updates the current series; otherwise the previous series is reused. Patamar is in `dados[1]`.
- Pre-allocates numpy array of size `MAX_PATAMARES * MAX_SERIES_SINTETICAS` rows
- Produces DataFrame with columns `["ano", "serie", "patamar"] + MESES_DF`, formatted via `formata_df_meses_para_datas_nwlistop()`

Typical subclass (`CmargsAnos` in `inewave/nwlistop/modelos/cmarg.py`):

```python
class CmargsAnos(ValoresSeriePatamar):
    __slots__ = []
    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [IntegerField(4, 2), IntegerField(2, 9)]
        + [FloatField(11, 14 + 11 * i, 2) for i in range(len(MESES_DF))]
    )
```

The `DATA_LINE` always has: `[IntegerField for serie, IntegerField/LiteralField for patamar] + [FloatField * 12 for months]`.

**Key difference from ValoresSerie**: The series tracking logic -- when a series field reads as `None` (blank), the previous series value is carried forward. This groups multiple patamar rows under the same series number.

## Specification

### Requirements

1. Create `TabelaSeriePatamarAnual` class in `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py`
2. Must extend `Block` and compose `TabularParser` internally (same architectural pattern as ticket-004's `TabelaSerieAnual`)
3. Must preserve the exact same series-tracking behavior: when the series column value is `None`, carry forward the last non-None series value
4. Must produce a DataFrame with columns: `data` (datetime), `patamar` (str/int), `serie` (int), `valor` (float) -- matching the output of `formata_df_meses_para_datas_nwlistop()`
5. Subclasses override `COLUMNS` (list of `ColumnDef`) -- the convention is: first ColumnDef is "serie", second is "patamar", remaining 12 are months
6. Write comprehensive unit tests with output equivalence verification

### Inputs/Props

- `COLUMNS`: list of `ColumnDef` -- column definitions (replacing `DATA_LINE`)
- `YEAR_LINE`: `Line` instance for reading the year from the header (default: `Line([IntegerField(4, 10)])`)
- `BEGIN_PATTERN`: `"     ANO: "` (for Block pattern matching)
- `END_PATTERN`: `" MEDIA"` (note: slightly different from ValoresSerie's `"MEDIA "`)

### Outputs/Behavior

- `self.data` after `read()`: a pandas DataFrame identical to what `ValoresSeriePatamar` produces
- Series carry-forward logic must be preserved exactly

### Error Handling

- Same as ticket-004: parse errors produce None-filled rows via `TabularParser`
- If year cannot be parsed, raise the same error as the current `Line.read()`

## Acceptance Criteria

- [ ] Given `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py`, when I read it, then it contains `TabelaSeriePatamarAnual` extending `Block` with `TabularParser` composition
- [ ] Given a subclass with the same fields as `CmargsAnos`, when I feed it the cmarg mock data, then the output DataFrame is identical to `ValoresSeriePatamar` output
- [ ] Given input data where series numbers are blank on patamar continuation rows, when I read it, then the series column correctly carries forward the last non-None value
- [ ] Given the test suite, when I run the new tests, then all pass and demonstrate output equivalence

## Implementation Guide

### Suggested Approach

1. Create `TabelaSeriePatamarAnual` following the same architecture as `TabelaSerieAnual` (ticket-004):
   - Extend `Block`
   - Compose `TabularParser` with `self.__class__.COLUMNS`
   - Custom `read()` that:
     a. Reads year from header
     b. Skips separator line
     c. Reads data lines via `TabularParser.parse_lines()`
     d. Post-processes with series carry-forward logic
     e. Adds year and patamar columns
     f. Applies `formata_df_meses_para_datas_nwlistop()`

2. The series carry-forward logic in post-processing:

```python
# After parsing
parsed = self._parser.parse_lines(lines)
series_col = parsed["serie"]
current_series = None
for i, val in enumerate(series_col):
    if val is not None:
        current_series = val
    else:
        series_col[i] = current_series if current_series is not None else 1
```

3. Build DataFrame from parsed dict, add year, reorder columns, apply formatting

### Key Files to Modify

- **Create**: `/home/rogerio/git/inewave/inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py`
- **Create**: `/home/rogerio/git/inewave/tests/nwlistop/test_tabela_serie_patamar_anual.py`
- **Read (reference)**: `/home/rogerio/git/inewave/inewave/nwlistop/modelos/blocos/valoresseriepatamar.py`
- **Read (reference)**: `/home/rogerio/git/inewave/inewave/nwlistop/modelos/cmarg.py` (typical subclass)
- **Read (reference)**: `/home/rogerio/git/inewave/tests/mocks/arquivos/cmarg.py` (mock data)

### Patterns to Follow

- Same composition pattern as ticket-004's `TabelaSerieAnual`
- Same `__eq__` pattern using `pd.DataFrame.equals()`
- Same test pattern: mock data from `tests/mocks/arquivos/`

### Pitfalls to Avoid

- Do NOT forget the series carry-forward logic -- this is the critical difference from `TabelaSerieAnual`
- The `END_PATTERN` is `" MEDIA"` (with leading space) for `ValoresSeriePatamar`, vs `"MEDIA "` (trailing space) for `ValoresSerie` -- preserve this difference
- Some subclasses use `IntegerField` for patamar, others use `LiteralField` -- the COLUMNS definition must accommodate both
- Do NOT change the DataFrame column order or dtypes

## Testing Requirements

### Unit Tests

Create `tests/nwlistop/test_tabela_serie_patamar_anual.py`:

1. Test with `CmargsAnos` field definitions and cmarg mock data
2. Test series carry-forward with multi-patamar data
3. Test `__eq__` method
4. Test with empty data
5. Verify exact DataFrame equivalence with `ValoresSeriePatamar` output

### Integration Tests

Temporarily wire `Cmarg` to use the new base class and run `tests/nwlistop/test_cmarg.py`.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-003 (depends on cfinterface >= 1.9.0 being verified)
- **Blocks**: ticket-007, ticket-010, ticket-011, ticket-012

## Effort Estimate

**Points**: 5
**Confidence**: Medium (series carry-forward logic adds complexity)
