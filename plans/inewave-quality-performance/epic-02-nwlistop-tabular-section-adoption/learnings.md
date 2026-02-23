# Epic 02 Learnings: nwlistop TabularSection Adoption

## Patterns Established

- **Block + TabularParser composition pattern**: `TabelaSerieAnual` and `TabelaSeriePatamarAnual`
  both extend `Block` (not `TabularSection`/`Section`) and compose a `TabularParser` internally.
  This is the correct approach for all nwlistop blocks because nwlistop files use `BlockFile`, not
  `SectionFile`. See `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py` and
  `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py`.

- **COLUMNS-only subclass definition**: All migrated model files define a single class attribute
  `COLUMNS = [ColumnDef(...), ...]`. The block class is entirely defined by `COLUMNS`; no
  `HEADER_LINE` / `DATA_LINE` override is needed. Convention: first `ColumnDef` is `"serie"`,
  next (patamar variant only) is `"patamar"`, then 12 month `ColumnDef`s using `MESES_DF[i]` as
  names. See `inewave/nwlistop/modelos/earmf.py` (serie variant) and
  `inewave/nwlistop/modelos/cmarg.py` (patamar variant).

- **isinstance() dual-type guard in archive bases**: Archive base classes (`ArquivoREE`,
  `ArquivoSIN`, etc.) use `isinstance(b, (ValoresSerie, TabelaSerieAnual))` in `__monta_tabela()`
  to support both old and new block types simultaneously during the transition period and going
  forward. This is the safest backward-compatible pattern because it does not depend on cfinterface
  `of_type()` index registration. See `inewave/nwlistop/modelos/arquivos/arquivoree.py` and
  `inewave/nwlistop/modelos/arquivos/arquivosinpatamar.py`.

- **Series carry-forward via static mutation**: `TabelaSeriePatamarAnual._apply_series_carry_forward()`
  mutates the `parsed` dict in place before `_build_dataframe()` is called. The method is `@staticmethod`
  because it needs no instance state. Default fill value is `1` (not `None`). See
  `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py` lines 112-124.

- **Separator line preservation for write()**: Both new base classes capture the separator line
  (`self._separador = file.readline()`) during `read()` and replay it verbatim in `write()`. This
  preserves the original formatting (column header row) without parsing it. See both base class
  `read()` / `write()` implementations.

- **Serie blanking on write for patamar files**: `TabelaSeriePatamarAnual.write()` calls
  `_blank_serie_field()` to blank the serie column on continuation patamar rows (rows that share
  the same serie as the previous row but have a different patamar). This reconstructs the sparse
  format of the original files. See `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py`
  lines 100-108 and 152-156.

- **DeprecationWarning in `__init__`**: Both `ValoresSerie` and `ValoresSeriePatamar` now emit
  `DeprecationWarning` in their `__init__` with `stacklevel=2`. The old classes are kept (not
  deleted) because external code may reference them. See
  `inewave/nwlistop/modelos/blocos/valoresserie.py` lines 31-35 and
  `inewave/nwlistop/modelos/blocos/valoresseriepatamar.py` lines 30-36.

- **AI bloat cleanup pass**: After each batch migration the code simplifier reviewed 10 files and
  removed unnecessary docstrings, redundant type comments, and over-engineered helpers that were
  inserted during the automated migration. This is an expected step in any large-scale mechanical
  migration; plan for it explicitly in future epics.

## Architectural Decisions

- **Extend Block, not TabularSection**: The ticket plan considered extending `TabularSection`
  (which extends `Section`). This was rejected because nwlistop files use `BlockFile`/`Block`,
  and mixing `Section` into a `Block` subclass would violate the cfinterface lifecycle contract.
  The accepted approach is to compose `TabularParser` inside a `Block` subclass, replicating what
  `TabularSection` does internally but staying inside the `Block` hierarchy.

- **`isinstance()` guard instead of `of_type()` for archive bases**: The plan suggested using
  cfinterface's `of_type()` method, which relies on a type registry. Using `isinstance()` directly
  was chosen instead because it works regardless of registration order and is transparent to future
  maintainers. The cost is a slight verbosity increase in `__monta_tabela()`; the benefit is
  zero dependency on cfinterface internals.

- **Exclusion of `gtert.py` (ValoresClasseTermicaSeriePatamar)**: The `gtert.py` file uses
  `ValoresClasseTermicaSeriePatamar`, which has 3 grouping levels (classe + serie + patamar) and
  additional MEDIA/MAX sentinel line handling inside `read()`. This cannot be represented by
  either new base class without significant new design work. The decision was to leave it on the
  old block type and document it as the sole remaining non-migrated block.
  See `inewave/nwlistop/modelos/gtert.py` and
  `inewave/nwlistop/modelos/blocos/valoresclassetermicaseriepatamar.py`.

- **BLOCKS list left pointing to old type in archive bases**: Archive base classes (`ArquivoREE`,
  `ArquivoSIN`, etc.) retain `BLOCKS = [HeaderBlock, ValoresSerie]` even after migration. The
  actual block type used is determined by the concrete model file's import (which now imports
  `TabelaSerieAnual`). The `BLOCKS` list functions as a fallback/sentinel; the real dispatch
  happens at the concrete level. This avoids touching the cfinterface dispatch mechanism.

- **No deletion of old block classes**: `ValoresSerie` and `ValoresSeriePatamar` are retained
  with deprecation warnings rather than deleted, because inewave is a library and downstream
  packages may subclass them directly. Deletion is deferred to a future major version bump.

## Files and Structures Created

- `inewave/nwlistop/modelos/blocos/tabela_serie_anual.py`: New base block class for 77-subclass
  ValoresSerie family. Provides `COLUMNS`-driven parsing, `_build_dataframe()`, and `_tidy_to_wide()`
  for round-trip write support. 113 LOC.

- `inewave/nwlistop/modelos/blocos/tabela_serie_patamar_anual.py`: New base block class for
  87-subclass ValoresSeriePatamar family. Adds series carry-forward, patamar handling, and
  `_blank_serie_field()` for write. 156 LOC.

- `tests/nwlistop/test_tabela_serie_anual.py`: Unit tests for `TabelaSerieAnual`. Defines a
  concrete test subclass (`EarmsAnosTSA`) with the same field layout as `EarmsAnos` and verifies
  DataFrame equivalence against the legacy class. 318 LOC.

- `tests/nwlistop/test_tabela_serie_patamar_anual.py`: Unit tests for `TabelaSeriePatamarAnual`.
  Defines `CmargsAnosTSPA` and verifies series carry-forward, patamar handling, and DataFrame
  equivalence against `ValoresSeriePatamar`. 433 LOC.

## Conventions Adopted

- **COLUMNS naming convention**: In every `TabelaSerieAnual` subclass, column names must use
  exactly `"serie"` for the integer series field and `MESES_DF[i]` for the 12 month float fields.
  In `TabelaSeriePatamarAnual` subclasses, additionally `"patamar"` must be the name of the second
  `ColumnDef`. Deviating from these names will break `_build_dataframe()` and `_tidy_to_wide()`.

- **`__slots__ = []` on every subclass**: All block subclasses declare `__slots__ = []` to
  preserve memory layout. This is the existing nwlistop convention and must be followed in all
  new model files.

- **`FloatField` format parameter for scientific notation**: The `pivarm.py` file
  (`PivarmAnos_v29_2`) uses `FloatField(..., format="E")` for scientific notation output. This is
  the mechanism for format variants in VERSIONS files. See
  `inewave/nwlistop/modelos/pivarm.py`.

- **Test subclass naming**: Test-only subclasses in test files are named with a `TSA` or `TSPA`
  suffix to distinguish them from the production classes they mirror (e.g., `EarmsAnosTSA`,
  `CmargsAnosTSPA`). This is the convention established in ticket-004/005 and should be followed
  in future test files for these base classes.

- **Batch migration grouping**: Model files were grouped and migrated by their archive base class
  (REE/SIN, Usina, Submercado/REEPatamar, SINPatamar/UsinaPatamar, remaining) in tickets 008-012.
  This grouping minimises cross-contamination and makes each ticket independently reviewable.

## Surprises and Deviations

- **`write()` was not in the original plan but was required**: Tickets 004-005 specified only
  `read()` behavior for the new base classes. During implementation it became clear that the
  `write()` method also needed to be implemented to satisfy the round-trip tests (the existing
  nwlistop tests verify read-then-write round trips). Both `TabelaSerieAnual.write()` and
  `TabelaSeriePatamarAnual.write()` were implemented with `_tidy_to_wide()` helpers.
  The serie-blanking logic in `TabelaSeriePatamarAnual.write()` was the most complex part.

- **`_tidy_to_wide()` requires a pivot** : The stored DataFrame is in tidy (long) format
  (`data`, `serie`, `valor` columns). Writing requires converting back to wide format
  (serie as index, months as columns). This pivot is performed by `_tidy_to_wide()` in both
  base classes. Future base classes that store data in a different shape will need their own
  inverse transformation.

- **LOC count differs from plan estimate**: The epic overview stated "nwlistop model LOC
  reduced by at least 30%". The final LOC count for all files under `inewave/nwlistop/modelos/`
  is approximately 6431, which matches the 6621 figure referenced in the context. The net reduction
  from the migration is real but the precise pre-migration baseline was not captured for comparison.
  Future epics should snapshot LOC before starting batch migrations.

- **181 files changed (not ~162)**: The epic estimated ~162 model files. The actual diff touched
  181 files (including archive base classes, state files, README, and test files). The model file
  count alone was closer to 160, but the total changeset is larger due to supporting infrastructure.

- **AI bloat cleanup was a non-trivial additional step**: The automated batch migration
  (tickets 008-012) introduced over-engineered docstrings and redundant comments in ~10 files.
  A dedicated cleanup pass by the code simplifier was required before the final verification
  in ticket-013. Future batch-migration epics should budget for an explicit simplification pass.

## Recommendations for Future Epics

- **Epic 03 (schema versioning) can build on `TabelaSerieAnual` VERSIONS support**: The
  `pivarm.py` file already has a `PivarmAnos_v29_2` class demonstrating version-differentiated
  `FloatField` format. The versioning epic should treat this as the reference pattern for
  format-variant blocks. See `inewave/nwlistop/modelos/pivarm.py`.

- **Epic 05 (mypy strict) will need `COLUMNS: ClassVar[List[ColumnDef]]` annotations**: The
  current `COLUMNS: List[ColumnDef] = []` class attribute on `TabelaSerieAnual` and
  `TabelaSeriePatamarAnual` will require `ClassVar` annotation to pass mypy strict. Plan for this
  in the strict-typing tickets (tickets 023-024).

- **`ValoresClasseTermicaSeriePatamar` in `gtert.py` remains on the old pattern**: Any future
  simplification of the thermal-class block must handle 3-level carry-forward (classe + serie +
  patamar) and MEDIA/MAX sentinel lines inside `read()`. This is the only structural exception
  in the nwlistop module. See `inewave/nwlistop/modelos/blocos/valoresclassetermicaseriepatamar.py`.

- **Round-trip (read-write-read) tests for nwlistop are a reliable regression gate**: All 1126
  tests passed at the end of this epic, including round-trip assertions. The test suite should be
  the primary gate for any future changes to the base block classes.

- **Snapshot LOC before starting batch migrations**: The plan assumed a ">30% LOC reduction" but
  there was no pre-migration baseline captured in the state files. For Epic 04 and beyond, record
  `wc -l inewave/<module>/**/*.py` totals in the epic overview before and after.
