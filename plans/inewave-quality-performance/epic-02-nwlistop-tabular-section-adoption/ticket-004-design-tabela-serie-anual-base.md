# ticket-004 Design and implement TabelaSerieAnual TabularSection base class

## Context

### Background

The nwlistop module uses `ValoresSerie` (in `inewave/nwlistop/modelos/blocos/valoresserie.py`) as the base class for 77 block subclasses that parse year-grouped tabular data with series rows and monthly columns. Each subclass overrides only `HEADER_LINE` and `DATA_LINE` (both `Line` instances). The `ValoresSerie.read()` method manually constructs a numpy array, converts to DataFrame, and applies date formatting. This is exactly the kind of boilerplate that `TabularSection` from cfinterface v1.9.0 was designed to eliminate.

However, `TabularSection` alone cannot replace `ValoresSerie` because:

1. The year must be extracted from the header line (`"     ANO: XXXX"`)
2. The data must be post-processed: year column added, series column filled (1 for NaN), dates formatted via `formata_df_meses_para_datas_nwlistop()`
3. The output is a pandas DataFrame (not a dict-of-lists)

We need a new base class `TabelaSerieAnual` that extends `TabularSection` to handle these inewave-specific conventions.

### Relation to Epic

This is the first ticket in the TabularSection adoption sequence. It creates the foundation that all 77 ValoresSerie subclasses will be migrated to.

### Current State

`ValoresSerie` in `/home/rogerio/git/inewave/inewave/nwlistop/modelos/blocos/valoresserie.py`:

- `BEGIN_PATTERN = "     ANO: "`
- `END_PATTERN = "MEDIA "`
- `HEADER_LINE` and `DATA_LINE` are `Line([])` (overridden by subclasses)
- `read()`: reads year from header, loops data lines into numpy array, converts to DataFrame with columns `["serie"] + MESES_DF`, adds year column, formats dates
- `__eq__()`: compares DataFrames with `.equals()`
- Uses `MAX_SERIES_SINTETICAS` (2000) as numpy array size bound

Typical subclass example (`EarmsAnos` in `inewave/nwlistop/modelos/earmf.py`):

```python
class EarmsAnos(ValoresSerie):
    __slots__ = []
    HEADER_LINE = Line([IntegerField(4, 10)])
    DATA_LINE = Line(
        [IntegerField(4, 2)]
        + [FloatField(8, 8 + 9 * i, 1) for i in range(len(MESES_DF))]
    )
```

The `DATA_LINE` always has the pattern: `[IntegerField for serie] + [FloatField * 12 for months]`.
The `HEADER_LINE` always reads a single integer (the year).

## Specification

### Requirements

1. Create a new file `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py` containing the `TabelaSerieAnual` class
2. `TabelaSerieAnual` must extend `TabularSection` (from `cfinterface.components.tabular`)
3. It must preserve the exact same behavior as `ValoresSerie`:
   - Extract year from the first header line
   - Parse data lines using COLUMNS (replacing DATA_LINE)
   - Produce a pandas DataFrame with columns: `data` (datetime), `serie` (int), `valor` (float)
   - Apply `formata_df_meses_para_datas_nwlistop()` for date formatting
4. Subclasses must be able to override only `COLUMNS` (list of `ColumnDef`) instead of `HEADER_LINE`/`DATA_LINE`
5. The `BEGIN_PATTERN` and `END_PATTERN` should remain as class attributes for BlockFile pattern matching
6. Write comprehensive unit tests proving output equivalence with the original `ValoresSerie`

### Inputs/Props

- `COLUMNS`: list of `ColumnDef` -- the column definitions (replacing `DATA_LINE`)
- `HEADER_LINES`: set to 2 by default (year line + blank separator line in original format)
- `BEGIN_PATTERN`: `"     ANO: "` (inherited from BlockFile pattern matching, not TabularSection)
- `END_PATTERN`: `"MEDIA "` (used by both Block.ends() and TabularSection)

### Outputs/Behavior

- `self.data` after `read()`: a pandas DataFrame with columns `[data, serie, valor]` produced by `formata_df_meses_para_datas_nwlistop()`
- The DataFrame must be identical (column names, dtypes, values) to what `ValoresSerie` produces

### Error Handling

- If the year cannot be parsed from the header line, raise the same error as the current `Line.read()` would raise
- If a data line cannot be parsed, the `TabularParser` fills the row with None (existing behavior)

## Acceptance Criteria

- [ ] Given the file `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`, when I read it, then it contains a `TabelaSerieAnual` class that extends `TabularSection`
- [ ] Given a `TabelaSerieAnual` subclass with the same field definitions as `EarmsAnos`, when I feed it the same mock data as the `test_earmf.py` test, then `self.data` is a DataFrame identical to what `ValoresSerie` produces
- [ ] Given the `TabelaSerieAnual` class, when a subclass defines only `COLUMNS`, then `read()` and data production work correctly
- [ ] Given the test suite, when I run `pytest tests/nwlistop/test_earmf.py -v`, then all tests pass (proving backward compatibility)
- [ ] Given the new test file, when I run tests for `TabelaSerieAnual`, then output equivalence with `ValoresSerie` is verified on at least 3 representative mock datasets

## Implementation Guide

### Suggested Approach

1. Study the `TabularSection` implementation in `/home/rogerio/git/cfinterface/cfinterface/components/tabular.py`
2. Study the `ValoresSerie` implementation in `/home/rogerio/git/inewave/inewave/nwlistop/modelos/blocos/valoresserie.py`
3. Note the key difference: `TabularSection` extends `Section` (for `SectionFile`), but nwlistop uses `BlockFile` and `Block`. `TabelaSerieAnual` must extend `Block` (not `Section`) and compose a `TabularParser` internally, similar to how `TabularSection` does but adapted for the Block lifecycle.

**Critical design decision**: `TabularSection` extends `Section`, but nwlistop files use `BlockFile` with `Block` subclasses. Since `Block` and `Section` share the same lifecycle (`read(file)` / `write(file)`), the approach is:

- Create `TabelaSerieAnual` extending `Block`
- Compose a `TabularParser` internally (same pattern as `TabularSection`)
- Override `read()` to:
  a. Read the year from the first line using a dedicated year `Line`
  b. Skip the separator line
  c. Read data lines using `TabularParser.parse_lines()` until `END_PATTERN` or blank
  d. Post-process into DataFrame (add year, format dates)
- Override `write()` to reconstruct the output

```python
from cfinterface.components.block import Block
from cfinterface.components.tabular import ColumnDef, TabularParser
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from inewave._utils.formatacao import formata_df_meses_para_datas_nwlistop
from inewave.config import MESES_DF
import pandas as pd
from typing import IO, List, Any, Optional

class TabelaSerieAnual(Block):
    __slots__ = ["_parser", "_year_line", "_year"]

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = "MEDIA "

    # Subclasses override COLUMNS instead of DATA_LINE
    COLUMNS: List[ColumnDef] = []
    YEAR_LINE: Line = Line([IntegerField(4, 10)])

    def __init__(self, previous=None, next=None, data=None):
        super().__init__(previous, next, data)
        self._parser = TabularParser(self.__class__.COLUMNS)
        self._year_line = self.__class__.YEAR_LINE
        self._year: Optional[int] = None

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TabelaSerieAnual):
            return False
        if not all([
            isinstance(self.data, pd.DataFrame),
            isinstance(o.data, pd.DataFrame),
        ]):
            return False
        return self.data.equals(o.data)

    def read(self, file: IO, *args, **kwargs):
        # Read year from header line
        self._year = self._year_line.read(file.readline())[0]
        file.readline()  # skip separator line

        # Read data lines until END_PATTERN or blank
        lines: List[str] = []
        while True:
            line = file.readline()
            if self.ends(line) or len(line) <= 1:
                break
            lines.append(line)

        # Parse using TabularParser
        parsed = self._parser.parse_lines(lines)

        # Post-process into DataFrame
        cols = ["serie"] + MESES_DF
        df = pd.DataFrame(parsed)
        # Rename columns to match expected names
        # ... (map ColumnDef names to expected names)
        df["ano"] = self._year
        df.loc[df["serie"].isna(), "serie"] = 1
        df = df[["ano"] + cols]
        df = df.astype({"serie": "int64", "ano": "int64"})
        self.data = formata_df_meses_para_datas_nwlistop(df)
```

4. The exact column mapping depends on how subclasses define COLUMNS. The convention should be:
   - First ColumnDef: name="serie", field=IntegerField(...)
   - Remaining 12 ColumnDefs: name=MESES_DF[i], field=FloatField(...)

5. Write tests in `tests/nwlistop/test_tabela_serie_anual.py` that:
   - Create a TabelaSerieAnual subclass with the same fields as EarmsAnos
   - Feed it mock data from `tests/mocks/arquivos/earmf.py`
   - Compare output DataFrame with the original ValoresSerie output

### Key Files to Modify

- **Create**: `/home/rogerio/git/inewave/inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`
- **Create**: `/home/rogerio/git/inewave/tests/nwlistop/test_tabela_serie_anual.py`
- **Read (reference)**: `/home/rogerio/git/inewave/inewave/nwlistop/modelos/blocos/valoresserie.py`
- **Read (reference)**: `/home/rogerio/git/cfinterface/cfinterface/components/tabular.py`
- **Read (reference)**: `/home/rogerio/git/inewave/inewave/_utils/formatacao.py`

### Patterns to Follow

- Follow the `TabularSection` composition pattern from cfinterface: compose `TabularParser`, do not inherit from it
- Follow the `ValoresSerie` `__eq__` pattern: use `pd.DataFrame.equals()` for comparison
- Follow the existing test pattern: use mock data from `tests/mocks/arquivos/`

### Pitfalls to Avoid

- Do NOT extend `TabularSection` (which is a `Section`) -- extend `Block` instead, since nwlistop uses `BlockFile`
- Do NOT change the output DataFrame format -- it must be identical to `ValoresSerie` output
- Do NOT import pandas at module level in the new base class -- follow the same `import pandas as pd` pattern used in `valoresserie.py`
- The `formata_df_meses_para_datas_nwlistop` function is critical -- it converts month columns to datetime rows. Do not skip it.

## Testing Requirements

### Unit Tests

Create `tests/nwlistop/test_tabela_serie_anual.py`:

1. Test that a `TabelaSerieAnual` subclass with `EarmsAnos` fields produces identical DataFrame to `ValoresSerie`-based `EarmsAnos`
2. Test `__eq__` method
3. Test with empty data
4. Test with multiple year blocks (the archive base class handles this, but verify single-block works)

### Integration Tests

Temporarily wire `Earmf` to use the new base class and run `tests/nwlistop/test_earmf.py` to verify full round-trip compatibility.

### E2E Tests

Not applicable.

## Dependencies

- **Blocked By**: ticket-003
- **Blocks**: ticket-005, ticket-006, ticket-008, ticket-009

## Effort Estimate

**Points**: 5
**Confidence**: Medium (the year extraction and DataFrame post-processing require careful design)
