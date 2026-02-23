# Epic 02: nwlistop TabularSection Adoption

## Goals

1. Replace the manual `numpy` + `pandas` DataFrame construction in `ValoresSerie` and `ValoresSeriePatamar` base blocks with `TabularSection` subclasses
2. Simplify the 13 archive base classes (`ArquivoREE`, `ArquivoSIN`, etc.) to leverage `TabularSection.data` and `TabularParser.to_dataframe()`
3. Migrate the ~162 model files that subclass `ValoresSerie`/`ValoresSeriePatamar` to use `TabularSection` column definitions
4. Maintain 100% backward compatibility on all public properties (`.valores`, `.ree`, `.submercado`, `.usina`, etc.)

## Strategy

The nwlistop module has a highly regular structure. There are exactly 3 base block types that handle tabular data:

1. **`ValoresSerie`** (77 subclasses): Series data with columns `[serie, jan..dez]` per year block
2. **`ValoresSeriePatamar`** (87 subclasses): Series+patamar data with columns `[serie, patamar, jan..dez]` per year block
3. **`ValoresClasseTermicaSeriePatamar`** (1 subclass): Special variant for thermal class data

And 13 archive base classes that all implement the same `__monta_tabela()` pattern (loop over blocks, `pd.concat`).

The migration strategy is:

**Phase A -- Prototype and validate** (tickets 004-005):

- Create new `TabularSection`-based replacements for the 2 core block types
- Verify they produce identical output with one representative file per pattern

**Phase B -- Migrate archive base classes** (tickets 006-007):

- Update the 13 archive base classes to work with the new TabularSection blocks
- Simplify `__monta_tabela()` to use `TabularParser.to_dataframe()`

**Phase C -- Batch migrate model files** (tickets 008-012):

- Migrate all ~162 model files in batches grouped by base archive type
- Each batch touches files with identical structure (same HEADER_LINE/DATA_LINE pattern)

**Phase D -- Cleanup** (ticket 013):

- Remove old `ValoresSerie`/`ValoresSeriePatamar` classes if no longer used
- Run full test suite and verify

## Key Challenge: ValoresSerie read() Complexity

The current `ValoresSerie.read()` and `ValoresSeriePatamar.read()` methods do more than simple tabular parsing:

1. They read a year from the header line (`"     ANO: XXXX"`)
2. They loop reading data lines until `END_PATTERN` ("MEDIA") or blank line
3. They build a numpy array and then convert to DataFrame with specific column names and dtypes
4. `ValoresSeriePatamar` additionally tracks a "current series" that persists across rows within a patamar group

This is NOT a simple `TabularSection` drop-in. The `TabularSection` can handle the per-block parsing (header lines, end pattern, data lines), but the year extraction from the header and the DataFrame post-processing (date formatting via `formata_df_meses_para_datas_nwlistop`) must be preserved.

**Approach**: Create a new `TabelaSerieAnual` base class that extends `TabularSection` to handle:

- Year extraction from the `BEGIN_PATTERN` / header line
- Post-read DataFrame formatting (add year column, call `formata_df_meses_para_datas_nwlistop`)
- The patamar variant adds patamar column handling

## Tickets

| Ticket     | Title                                                                                         | Effort   |
| ---------- | --------------------------------------------------------------------------------------------- | -------- |
| ticket-004 | Design and implement TabelaSerieAnual TabularSection base class                               | 5 points |
| ticket-005 | Design and implement TabelaSeriePatamarAnual TabularSection base class                        | 5 points |
| ticket-006 | Migrate ValoresSerie archive base classes to use TabelaSerieAnual                             | 3 points |
| ticket-007 | Migrate ValoresSeriePatamar archive base classes to use TabelaSeriePatamarAnual               | 3 points |
| ticket-008 | Batch migrate ArquivoREE and ArquivoSIN model files (35 files)                                | 3 points |
| ticket-009 | Batch migrate ArquivoUsina model files (17 files)                                             | 2 points |
| ticket-010 | Batch migrate ArquivoSubm and ArquivoREEPatamar model files (47 files)                        | 3 points |
| ticket-011 | Batch migrate ArquivoSINPatamar and ArquivoUsinaPatamar model files (47 files)                | 3 points |
| ticket-012 | Batch migrate remaining archive types (Restricao, Bombeamento, ClasseTermica, PAR) (16 files) | 2 points |
| ticket-013 | Clean up deprecated block classes and run full verification                                   | 2 points |

## Dependencies

- **Blocked By**: Epic 01 (ticket-003)
- **Blocks**: Epic 03 (schema versioning benefits from simplified model structure)

## Success Criteria

- All 430+ existing tests pass
- All nwlistop model files use `TabularSection` subclasses (COLUMNS-based definition)
- The old `ValoresSerie`/`ValoresSeriePatamar` classes are either removed or deprecated
- No behavioral change in any public property (.valores, .ree, .submercado, etc.)
- nwlistop model LOC reduced by at least 30%
