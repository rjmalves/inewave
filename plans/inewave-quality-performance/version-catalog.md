# Version-Dependent File Catalog

## Version Key Convention

Version keys are **lexicographic strings** compared by `resolve_version()` in
`cfinterface/cfinterface/versioning.py`. The function iterates over
`sorted(versions.keys())` and returns the component list whose key is the
largest value `<= requested`. Comparison is standard Python string comparison,
not semantic versioning.

Important lexicographic ordering facts for the keys used in this codebase:

| Key        | After     | Before                |
| ---------- | --------- | --------------------- |
| `"27"`     | (oldest)  | `"28"`                |
| `"28"`     | `"27"`    | `"28.1"`              |
| `"28.1"`   | `"28"`    | `"28.12"`             |
| `"28.12"`  | `"28.1"`  | `"28.16"`             |
| `"28.16"`  | `"28.12"` | `"28.2"`              |
| `"28.2"`   | `"28.16"` | `"29"`                |
| `"29"`     | `"28.2"`  | `"29.2"`              |
| `"29.2"`   | `"29"`    | `"29.4"`              |
| `"29.4"`   | `"29.2"`  | `"29.4.1"`            |
| `"29.4.1"` | `"29.4"`  | `"30"` (hypothetical) |

Caution: `"28.2"` sorts **after** `"28.16"` (because `"2" > "1"` at position 3).
The existing codebase intentionally uses only keys where this ordering is
unambiguous for the versions it needs to distinguish.

Convention for handler classes: `BLOCKS` / `SECTIONS` is always the **latest
/ default** component list. `VERSIONS` maps **older** version key strings to
their specific component lists. The `BLOCKS` list itself need not appear in
`VERSIONS`, though some existing files repeat the latest key there for
documentation clarity.

---

## Already Versioned (5 files)

| Handler file                           | Model file                                     | Version keys                                                   | What changes between versions                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `inewave/nwlistop/cmarg.py`            | `inewave/nwlistop/modelos/cmarg.py`            | `"27"` (older), `"29.4.1"` (current default also in `BLOCKS`)  | Version `"27"`: `CmargsAnos27` with `FloatField(8, ...)` stride-9 columns; version `"29.4.1"`/default: `CmargsAnos` with `FloatField(11, ...)` stride-11 columns. Patamar-aware file (TabelaSeriePatamarAnual).                                                                                                                                                                                                                                              |
| `inewave/nwlistop/cmargmed.py`         | `inewave/nwlistop/modelos/cmargmed.py`         | `"28"` (older), `"29.4.1"` (current default also in `BLOCKS`)  | Version `"28"`: `CmargsAnos28` with `FloatField(8, 9 + 10*i, 2)`; version `"29.4.1"`/default: `CmargsAnos` with `FloatField(11, 9 + 11*i, 2)`. Series-only file (TabelaSerieAnual).                                                                                                                                                                                                                                                                          |
| `inewave/nwlistop/pivarm.py`           | `inewave/nwlistop/modelos/pivarm.py`           | `"28.12"` (older), `"29.2"` (current default also in `BLOCKS`) | Version `"28.12"`: `PivarmAnos` with `FloatField(15, ..., 2)` decimal format; version `"29.2"`/default: `PivarmAnos_v29_2` with `FloatField(15, ..., 7, format="E")` scientific notation.                                                                                                                                                                                                                                                                    |
| `inewave/nwlistop/pivarmincr.py`       | `inewave/nwlistop/modelos/pivarmincr.py`       | `"28.12"` (older), `"29.2"` (current default also in `BLOCKS`) | Identical pattern to `pivarm`: decimal vs. `format="E"` scientific notation in `FloatField`.                                                                                                                                                                                                                                                                                                                                                                 |
| `inewave/newave/avl_cortesfpha_nwv.py` | `inewave/newave/modelos/avl_cortesfpha_nwv.py` | `"28"` (older), `"28.16"` (current default also in `BLOCKS`)   | Version `"28"`: uses `VersaoModelo` block + `TabelaAvlCortesFpha28` (IntegerField size 5 for usina/periodo, `BEGIN_PATTERN` `"-----;-----;--------------;"`) ; version `"28.16"`/default: uses `VersaoModeloLibs` block + `TabelaAvlCortesFpha` (IntegerField size 4, `BEGIN_PATTERN` `"----;----;--------------;-------;"`). **Note**: This class is deprecated; `fpha_cortes.py` (`FphaCortes`) is the active replacement and uses only the latest format. |

---

## Needs VERSIONS -- nwlistop BlockFile (0 files)

After the Epic 02 tabular-section migration, the scan of all 170 nwlistop
handler files (`inewave/nwlistop/*.py`) and their model files
(`inewave/nwlistop/modelos/*.py`) found **no additional files** with version
variants beyond the 4 already versioned (`cmarg`, `cmargmed`, `pivarm`,
`pivarmincr`).

Evidence: the grep for model files with 2+ class definitions returned exactly:

```
inewave/nwlistop/modelos/cmargmed.py    -- CmargsAnos28, CmargsAnos (already versioned)
inewave/nwlistop/modelos/cmarg.py       -- CmargsAnos27, CmargsAnos (already versioned)
inewave/nwlistop/modelos/pivarmincr.py  -- PivarmAnos, PivarmAnos_v29_2 (already versioned)
inewave/nwlistop/modelos/pivarm.py      -- PivarmAnos, PivarmAnos_v29_2 (already versioned)
```

All other nwlistop model files define exactly one `TabelaSerieAnual` or
`TabelaSeriePatamarAnual` subclass. No additional version variants exist in the
current codebase.

---

## Needs VERSIONS -- newave SectionFile (0 files)

Scanning all `inewave/newave/*.py` handler files that extend `SectionFile`:

| Handler                | SECTIONS count       | Binary?    | Version variants found?                                                                                           |
| ---------------------- | -------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------- |
| `abertura.py`          | 1                    | No         | No                                                                                                                |
| `adterm.py`            | 1                    | No         | No                                                                                                                |
| `agrint.py`            | 2                    | No         | No -- 2 distinct section types for different data blocks in same file                                             |
| `arquivos.py`          | 1                    | No         | No                                                                                                                |
| `cadic.py`             | 1                    | No         | No                                                                                                                |
| `caso.py`              | 2                    | No         | No -- 2 distinct section types for different data                                                                 |
| `clast.py`             | 2                    | No         | No -- 2 distinct section types                                                                                    |
| `confhd.py`            | 1                    | No         | No                                                                                                                |
| `conft.py`             | 1                    | No         | No                                                                                                                |
| `cortesh.py`           | 1                    | **Binary** | No -- binary file, version stored as integer field `data[0]` read at parse time; not amenable to VERSIONS pattern |
| `cortes.py`            | 1                    | No         | No                                                                                                                |
| `curva.py`             | 7                    | No         | No                                                                                                                |
| `dger.py`              | ~107                 | No         | No confirmed variants -- see Open Questions                                                                       |
| `dsvagua.py`           | 1                    | No         | No                                                                                                                |
| `eafpast.py`           | 1                    | No         | No                                                                                                                |
| `eliminacao_cortes.py` | 1                    | No         | No                                                                                                                |
| `elnino.py`            | (N/A -- no SECTIONS) | No         | No                                                                                                                |
| `enavazb.py`           | 1                    | No         | No                                                                                                                |
| `enavazf.py`           | 1                    | No         | No                                                                                                                |
| `energiab.py`          | 1                    | **Binary** | No                                                                                                                |
| `energiaf.py`          | 1                    | **Binary** | No                                                                                                                |
| `energias.py`          | 1                    | **Binary** | No                                                                                                                |
| `engnat.py`            | 1                    | No         | No                                                                                                                |
| `ensoaux.py`           | (N/A -- no SECTIONS) | No         | No                                                                                                                |
| `exph.py`              | 1                    | No         | No                                                                                                                |
| `expt.py`              | 1                    | No         | No                                                                                                                |
| `forward.py`           | 1                    | **Binary** | No                                                                                                                |
| `forwarh.py`           | 1                    | **Binary** | No                                                                                                                |
| `ghmin.py`             | 1                    | No         | No                                                                                                                |
| `gtminpat.py`          | (N/A -- no SECTIONS) | No         | No                                                                                                                |
| `manutt.py`            | 1                    | No         | No                                                                                                                |
| `modif.py`             | (RegisterFile)       | No         | No                                                                                                                |
| `patamar.py`           | 4                    | No         | No confirmed variants -- see Open Questions                                                                       |
| `penalid.py`           | 1                    | No         | No                                                                                                                |
| `perda.py`             | (N/A -- no SECTIONS) | No         | No                                                                                                                |
| `re.py`                | 2                    | No         | No                                                                                                                |
| `ree.py`               | 2                    | No         | No                                                                                                                |
| `sar.py`               | (N/A -- no SECTIONS) | No         | No                                                                                                                |
| `selcor.py`            | 1                    | No         | No                                                                                                                |
| `shist.py`             | 2                    | No         | No                                                                                                                |
| `sistema.py`           | 5                    | No         | No confirmed variants -- see Open Questions                                                                       |
| `tecno.py`             | (N/A -- no SECTIONS) | No         | No                                                                                                                |
| `term.py`              | 1                    | No         | No                                                                                                                |
| `vazaob.py`            | 1                    | **Binary** | No                                                                                                                |
| `vazaof.py`            | 1                    | **Binary** | No                                                                                                                |
| `vazaos.py`            | 1                    | **Binary** | No                                                                                                                |
| `vazinat.py`           | 1                    | No         | No                                                                                                                |
| `vazoes.py`            | (RegisterFile)       | No         | No                                                                                                                |
| `vazpast.py`           | 1                    | No         | No                                                                                                                |
| `volref_saz.py`        | 1                    | No         | No                                                                                                                |

No newave `SectionFile` handlers require `VERSIONS` based on code and git
history analysis. All multi-section files use different section types to
represent structurally distinct blocks within the same file -- not version
variants of the same block.

---

## Needs VERSIONS -- newave BlockFile (0 files)

Scanning all `inewave/newave/*.py` handler files that extend `BlockFile` or
`ArquivoCSV`:

| Handler                 | BLOCKS                                                                               | VERSIONS already?           | Version variants found?                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------ | --------------------------- | -------------------------------------------------------------------------------------------- |
| `avl_cortesfpha_nwv.py` | `[VersaoModeloLibs, TabelaAvlCortesFpha]`                                            | **Yes** (already versioned) | See "Already Versioned" section                                                              |
| `avl_desvfpha_s.py`     | `[VersaoModelo, TabelaAvlDesvFphaS]`                                                 | No                          | No -- single TabelaCSV/Block subclass, no variant found                                      |
| `avl_desvfpha_v_q.py`   | `[VersaoModelo, TabelaAvlDesvFphaVQ]`                                                | No                          | No -- single Block subclass                                                                  |
| `cvar.py`               | `[BlocoValoresConstantesCVAR, BlocoAlfaVariavelNoTempo, BlocoLambdaVariavelNoTempo]` | No                          | No -- 3 distinct block types, not version variants                                           |
| `eco_fpha.py`           | `[VersaoModelo, TabelaEcoFpha]`                                                      | No                          | No -- single TabelaCSV subclass, deprecated wrapper                                          |
| `evap_avl_desv.py`      | `[VersaoModelo, TabelaAvlEvap]`                                                      | No                          | No                                                                                           |
| `evap_cortes.py`        | `[VersaoModelo, TabelaCortesEvap]`                                                   | No                          | No                                                                                           |
| `evap_eco.py`           | `[VersaoModelo, TabelaEcoEvap]`                                                      | No                          | No                                                                                           |
| `fpha_avl_desv_s.py`    | `[VersaoModelo, TabelaAvlDesvFphaS]`                                                 | No                          | No -- shares same block classes as `avl_desvfpha_s.py`                                       |
| `fpha_avl_desv_v_q.py`  | `[VersaoModelo, TabelaAvlDesvFphaVQ]`                                                | No                          | No                                                                                           |
| `fpha_cortes.py`        | `[VersaoModeloLibs, TabelaAvlCortesFpha]`                                            | No                          | No -- active replacement for deprecated `avl_cortesfpha_nwv.py`; uses only the latest format |
| `fpha_eco.py`           | `[VersaoModelo, TabelaEcoFpha]`                                                      | No                          | No                                                                                           |
| `newavetim.py`          | `[BlocoVersaoModeloTim, BlocoTemposEtapasTim]`                                       | No                          | No -- 2 distinct block types                                                                 |
| `nwv_avl_evap.py`       | `[VersaoModelo, TabelaAvlEvap]`                                                      | No                          | No                                                                                           |
| `nwv_cortes_evap.py`    | `[VersaoModelo, TabelaCortesEvap]`                                                   | No                          | No                                                                                           |
| `nwv_eco_evap.py`       | `[VersaoModelo, TabelaEcoEvap]`                                                      | No                          | No                                                                                           |
| `parpeol.py`            | 6 blocks                                                                             | No                          | No -- distinct block types                                                                   |
| `parp.py`               | 9 blocks                                                                             | No                          | No -- distinct block types                                                                   |
| `parpvaz.py`            | 9 blocks                                                                             | No                          | No -- distinct block types                                                                   |
| `pmo.py`                | 22 blocks                                                                            | No                          | No confirmed variants -- see Open Questions                                                  |

No newave `BlockFile` handlers (beyond the already-versioned
`avl_cortesfpha_nwv.py`) require `VERSIONS` based on code and git history
analysis.

---

## Needs VERSIONS -- newave RegisterFile (0 files)

| Handler     | REGISTERS                                                                                                                                 | Version variants found? |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `hidr.py`   | `[RegistroUHEHidr]`                                                                                                                       | No                      |
| `modif.py`  | `[ModifRegister, USINA, VOLMIN, VOLMAX, NUMCNJ, NUMMAQ, VAZMIN, CFUGA, CMONT, VMAXT, VMINT, VMINP, VAZMINT, VAZMAXT, TURBMAXT, TURBMINT]` | No                      |
| `vazoes.py` | `[RegistroVazoesPostos]`                                                                                                                  | No                      |

---

## No Versioning Needed

The following categories of files have been confirmed to not require `VERSIONS`
dictionaries based on inspection of their model files and git history.

### nwlistop BlockFile handlers (166 files, excluding 4 already versioned)

All remaining nwlistop handler files use a single `TabelaSerieAnual` or
`TabelaSeriePatamarAnual` subclass (one class per model file). Their
`FloatField` widths and strides are uniform across all known NEWAVE versions.
Evidence: the complete grep for model files with 2+ class definitions returned
only the 4 already-versioned files.

Categories within the 166 unversioned nwlistop handlers:

1. **Energy/flow quantities per REE**: `eaf.py`, `eafb.py`, `eafbm.py`,
   `eafbsin.py`, `eafm.py`, `earmf.py`, `earmfm.py`, `earmfp.py`,
   `earmfpm.py`, `earmfpsin.py`, `earmfsin.py` -- single `TabelaSerieAnual`
   subclass, no known version differences.

2. **Generation and turbine quantities per UHE**: `ghiduh.py`, `ghidr.py`,
   `ghidrm.py`, `ghidrsin.py`, `ghmax.py`, `ghmaxm.py`, `ghmaxmr.py`,
   `ghmaxr.py`, `ghmaxrsin.py`, `ghmaxsin.py`, `ghtot.py`, `ghtotm.py`,
   `ghtotsin.py`, `gtert.py`, `gttot.py`, `gttotsin.py`, `gh_fphexat.py`,
   `ghmax_fpha.py`, `ghmax_fphc.py`, `geol.py`, `geolm.py`, `geolsin.py`,
   `fteolm.py`, `fteolsin.py` -- single patamar-aware block, no variants.

3. **Cost quantities**: `cbomb.py`, `cbombsin.py`, `cdef.py`, `cdefsin.py`,
   `celetricas.py`, `coper.py`, `corteolm.py`, `cterm.py`, `ctermsin.py`,
   `custo_futuro.py`, `cviol_eletrica.py`, `cviol_eletricasin.py`,
   `cviol_rhq.py`, `cviol_rhq_sin.py`, `cviol_rhv.py`, `cviol_rhv_sin.py`,
   `c_v_rhq.py`, `c_v_rhq_s.py`, `c_v_rhv.py`, `c_v_rhv_s.py` -- single
   block, no variants.

4. **Violation quantities**: `viol_eletrica.py`, `viol_eletricasin.py`,
   `viol_evmin.py`, `viol_evminm.py`, `viol_evminsin.py`, `viol_fpha.py`,
   `viol_ghmin.py`, `viol_ghminm.py`, `viol_ghminsin.py`, `viol_ghminuh.py`,
   `viol_lpp_dfmax.py`, `viol_lpp_dfmaxm.py`, `viol_lpp_dfmaxsin.py`,
   `viol_lpp_tbmax.py`, `viol_lpp_tbmaxm.py`, `viol_lpp_tbmaxsin.py`,
   `viol_neg_evap.py`, `viol_neg_vretiruh.py`, `viol_pos_evap.py`,
   `viol_pos_vretiruh.py`, `viol_rhq.py`, `viol_rhv.py`, `viol_turbmax.py`,
   `viol_turbmin.py`, `viol_vazmax.py`, `viol_vazmin.py` -- single block,
   added in the v29.3 commit but with no older variant format.

5. **Deficit, market, and load-shedding**: `deficit.py`, `defsin.py`,
   `deletricas.py`, `depminuh.py`, `desvuh.py`, `dnegevap.py`, `dposevap.py`,
   `dtbmax.py`, `dtbmin.py`, `dvazmax.py` -- single block, no variants.

6. **Hydraulic state quantities per UHE**: `hjus.py`, `hliq.py`, `hmont.py`,
   `invade.py`, `invadem.py`, `mercl.py`, `merclsin.py`, `mevmin.py`,
   `mevminm.py`, `mevminsin.py`, `perdf.py`, `perdfm.py`, `perdfsin.py`,
   `qafluh.py`, `qbomb.py`, `qdesviouh.py`, `qincruh.py`, `qturuh.py`,
   `qvertuh.py`, `vagua.py`, `valor_agua.py`, `varmpuh.py`, `varmuh.py`,
   `vbomb.py`, `vdesviouh.py`, `vento.py`, `vertuh.py`, `verturbm.py`,
   `verturb.py`, `verturbsin.py`, `vevapuh.py`, `vevmin.py`, `vevminm.py`,
   `vevminsin.py`, `vghmin.py`, `vghminm.py`, `vghminsin.py`, `vghminuh.py`,
   `vmort.py`, `vmortm.py`, `vmortsin.py`, `vretiradauh.py`, `vturuh.py`,
   `dfphauh.py`, `edesvc.py`, `edesvcm.py`, `edesvcsin.py`, `evapo.py`,
   `evapom.py`, `evaporsin.py`, `evert.py`, `evertm.py`, `evertsin.py`,
   `exces.py`, `excessin.py` -- single block, no variants.

7. **LPP restriction quantities**: `dlppdfmax.py`, `dlppdfmaxm.py`,
   `dlppdfmaxs.py`, `dlpptbmax.py`, `dlpptbmaxm.py`, `dlpptbmaxs.py`,
   `dflppdfmaxm.py`, `dflpptbmaxm.py`, `rhslppdf.py`, `rhslpptb.py`,
   `form_rhq.py`, `form_rhv.py`, `intercambio.py` -- single patamar-aware
   block, no variants.

8. **MEDIAS-\*.CSV files** (CSV format, SectionFile): `mediasmerc.py`,
   `mediasree.py`, `mediasrep.py`, `mediasrhq.py`, `mediasrhv.py`,
   `mediassin.py`, `mediasusie.py`, `mediasusih.py`, `mediasusit.py` -- use
   `pd.read_csv()` for dynamic column reading; column schema adapts
   automatically to whatever NEWAVE version produces; no fixed VERSIONS
   pattern applicable.

9. **Input configuration file**: `nwlistopdat.py` -- single `BlocoDadosNwlistop`
   section with no known version differences.

### newave SectionFile handlers

The following are text-based SectionFile handlers with no known version
differences between NEWAVE versions:

- `abertura.py`, `adterm.py`, `agrint.py`, `arquivos.py`, `cadic.py`,
  `caso.py`, `clast.py`, `confhd.py`, `conft.py`, `cortes.py`, `curva.py`,
  `dsvagua.py`, `eafpast.py`, `eliminacao_cortes.py`, `enavazb.py`,
  `enavazf.py`, `engnat.py`, `exph.py`, `expt.py`, `ghmin.py`, `manutt.py`,
  `patamar.py`, `penalid.py`, `re.py`, `ree.py`, `selcor.py`, `shist.py`,
  `sistema.py`, `term.py`, `vazinat.py`, `vazpast.py`, `volref_saz.py`

### newave SectionFile handlers (binary)

Binary files whose section structure is not subject to the text-level VERSIONS
pattern:

- `cortesh.py` (`StorageType.BINARY`): version number stored as integer field
  within the binary record itself; parsed unconditionally.
- `energiab.py`, `energiaf.py`, `energias.py`, `forward.py`, `forwarh.py`,
  `vazaob.py`, `vazaof.py`, `vazaos.py` (`StorageType.BINARY`): binary layout
  with version-adaptive logic embedded in the single section's `read()` method.

### newave BlockFile handlers

- `avl_desvfpha_s.py`, `avl_desvfpha_v_q.py` -- deprecated; single block type.
- `cvar.py` -- 3 distinct structural block types, not version variants.
- `eco_fpha.py`, `evap_avl_desv.py`, `evap_cortes.py`, `evap_eco.py`,
  `fpha_avl_desv_s.py`, `fpha_avl_desv_v_q.py`, `fpha_cortes.py`,
  `fpha_eco.py`, `nwv_avl_evap.py`, `nwv_cortes_evap.py`, `nwv_eco_evap.py`
  -- CSV-style files with single table block; no version variants found.
- `newavetim.py` -- 2 distinct structural block types, not version variants.
- `parpeol.py`, `parp.py`, `parpvaz.py` -- multiple distinct block types for
  different sections of the same file; no version variants.
- `pmo.py` -- 22 distinct structural block types; no version variant model
  classes found; see Open Questions.

### newave RegisterFile handlers

- `hidr.py`, `modif.py`, `vazoes.py` -- single register types; no version
  variants.

### newave handlers with no SECTIONS/BLOCKS (utility files)

- `bid.py`, `clasgas.py`, `elnino.py`, `ensoaux.py`, `gee.py`, `gtminpat.py`,
  `itaipu.py`, `perda.py`, `sar.py`, `tecno.py` -- these are either pure
  utility modules or RegisterFile subclasses that lack their own format
  variation exposure.

---

## Open Questions / Unknowns

The following represent format changes that are **suspected** or **cannot be
fully confirmed** from code inspection and git history alone. They require
inspection of actual NEWAVE output files from different versions to confirm.

### 1. `inewave/newave/dger.py` -- Dger (SectionFile, ~107 sections)

**Status**: Suspected -- not confirmed.

`Dger` reads the `dger.dat` input configuration file. It has approximately 107
distinct `Section` subclasses in its `SECTIONS` list, corresponding to every
NEWAVE input keyword. NEWAVE has added new keywords across versions (e.g.,
`CALCULA_PRODT_MEDIA_SIN`, `APROVEITAMENTO_BASE_PLS_BACKWARD`,
`SEMENTE_FORWARD`, `SEMENTE_BACKWARD` appear to be recent additions based on
their position at the end of `modelos/dger.py`).

**Risk**: Files from older NEWAVE versions (pre-28) may not contain the newer
keywords. Because `SectionFile` matching is keyword-based (each `Section` has
a `BEGIN_PATTERN`), missing keywords are simply skipped -- they do not cause
parse errors. This means `Dger` likely already degrades gracefully for older
files without needing `VERSIONS`. The sections simply return `None` for
properties not present in older files.

**Conclusion**: Probably does not need `VERSIONS`. Confirm by attempting to
parse a pre-28 `dger.dat` with the current handler.

### 2. `inewave/newave/pmo.py` -- Pmo (BlockFile, 22 blocks)

**Status**: Suspected -- not confirmed.

`Pmo` reads `pmo.dat`, the NEWAVE execution summary. The 22 blocks
correspond to different output sections. Some blocks (e.g.,
`BlocoPenalidadeViolacaoEvaporacaoPMO`, `BlocoPenalidadeViolacaoFphaPMO`) were
added in newer versions and may not appear in older `pmo.dat` files.

**Risk**: Same as `Dger` -- `BlockFile` uses `BEGIN_PATTERN` matching and
silently skips unrecognized blocks. Missing blocks return `None` from their
properties. Probably degrades gracefully without `VERSIONS`.

**Conclusion**: Probably does not need `VERSIONS`. Confirm by testing against a
pre-28 `pmo.dat`.

### 3. `inewave/newave/patamar.py` -- Patamar (SectionFile, 4 sections)

**Status**: Suspected -- not confirmed.

`Patamar` reads `patamar.dat` which configures load duration curves. The
`BlocoUsinasNaoSimuladas` section was added to handle non-simulated plants in
newer configurations. Older versions of `patamar.dat` may not have this
section.

**Conclusion**: Probably degrades gracefully (keyword-based matching). Confirm
by testing against older NEWAVE versions.

### 4. `inewave/newave/sistema.py` -- Sistema (SectionFile, 5 sections)

**Status**: Suspected -- not confirmed.

`Sistema` reads `sistema.dat` and contains
`BlocoGeracaoUsinasNaoSimuladas` (non-simulated plant generation block), which
may not appear in older NEWAVE versions. Same keyword-based matching applies.

**Conclusion**: Probably degrades gracefully. Confirm by testing.

### 5. nwlistop files added in v29.3

The git commit `4c9a0066 atualiza arquivos 29.3` introduced ~70 new nwlistop
handler files and their corresponding model files. These files were created for
NEWAVE version 29.3 and have no older format variant in the codebase. They do
not need `VERSIONS` because they simply do not exist in older NEWAVE versions.

If users need to parse output from older versions that lack these files, the
expected behavior is that `inewave` raises a file-not-found error rather than a
parse error -- which is acceptable.

### 6. `fpha_cortes.py` -- FphaCortes and older `avl_cortesfpha_nwv.py`

**Status**: Confirmed non-issue.

`FphaCortes` is the active replacement for the deprecated `AvlCortesFpha` (in
`avl_cortesfpha_nwv.py`). `FphaCortes` always uses the latest format
(`VersaoModeloLibs` + `TabelaAvlCortesFpha`). The deprecated `AvlCortesFpha`
already has `VERSIONS`. No additional changes needed for `fpha_cortes.py`.

---

## Summary

| Category                                  | Count | Needs VERSIONS                     |
| ----------------------------------------- | ----- | ---------------------------------- |
| Already versioned                         | 5     | Yes (done)                         |
| nwlistop BlockFile -- needs VERSIONS      | **0** | N/A                                |
| newave SectionFile -- needs VERSIONS      | **0** | N/A                                |
| newave BlockFile -- needs VERSIONS        | **0** | N/A                                |
| newave RegisterFile -- needs VERSIONS     | **0** | N/A                                |
| Open questions (suspected, not confirmed) | 4     | Investigate before tickets 015/016 |
| No versioning needed (confirmed)          | ~246  | N/A                                |

**Key finding**: The current codebase already correctly handles all confirmed
format differences via `VERSIONS`. The 5 existing versioned files cover all
cases where model files define multiple class variants. All other files use
single-format model classes with no variant classes present in the codebase.

The main recommendation for tickets 015 and 016 is: **no new `VERSIONS`
dictionaries are needed** based on the current code. The open questions (dger,
pmo, patamar, sistema) should be investigated against real files from older
NEWAVE versions before deciding whether to add VERSIONS.
