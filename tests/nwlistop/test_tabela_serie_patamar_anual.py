"""
Unit tests for TabelaSeriePatamarAnual.

A concrete subclass (CmargsAnosTSPA) is defined here with the same field
layout as CmargsAnos so we can compare DataFrames produced by both classes
on identical input data.
"""

import io
from datetime import datetime

import pandas as pd
import pytest
from cfinterface.components.floatfield import FloatField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.tabular import ColumnDef

from inewave.config import MESES_DF
from inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual import (
    TabelaSeriePatamarAnual,
)
from inewave.nwlistop.modelos.cmarg import CmargsAnos

# ---------------------------------------------------------------------------
# Concrete test subclass — same field layout as CmargsAnos
# ---------------------------------------------------------------------------

_FLOAT_FIELDS_CMARG = [
    FloatField(11, 14 + 11 * i, 2) for i in range(len(MESES_DF))
]

CMARG_COLUMNS = [
    ColumnDef("serie", IntegerField(4, 2)),
    ColumnDef("patamar", IntegerField(2, 9)),
] + [
    ColumnDef(MESES_DF[i], _FLOAT_FIELDS_CMARG[i]) for i in range(len(MESES_DF))
]


class CmargsAnosTSPA(TabelaSeriePatamarAnual):
    """Test subclass mirroring CmargsAnos field layout."""

    __slots__: list = []

    COLUMNS = CMARG_COLUMNS


# ---------------------------------------------------------------------------
# Mock data — column-header separator used by this file format
# ---------------------------------------------------------------------------

_SEP = (
    "        PAT             1          2          3"
    "          4          5          6          7          8"
    "          9         10         11         12      MEDIA \n"
)

# Dataset 1: two series, three patamares — tests basic carry-forward
_MOCK_BLOCK_2024 = (
    "     ANO: 2024\n"
    + _SEP
    + "     1    1          0.00       0.00       0.00       0.00"
    "       0.00      22.54      52.38      75.12      53.17"
    "      93.48     113.19      97.72      72.52\n"
    + "          2          0.00       0.00       0.00       0.00"
    "       0.00      21.49      50.87      73.90      51.23"
    "      91.66     113.19      96.44      71.25\n"
    + "          3          0.00       0.00       0.00       0.00"
    "       0.00      21.21      50.22      71.18      48.43"
    "      89.04     110.03      96.44      69.51\n"
    + "     2    1          0.00       0.00       0.00       0.00"
    "       0.00      48.35      54.45      81.01      71.93"
    "      79.27      92.58      53.05      68.66\n"
    + "          2          0.00       0.00       0.00       0.00"
    "       0.00      46.10      51.10      76.04      68.96"
    "      76.11      91.76      52.98      66.15\n"
    + "          3          0.00       0.00       0.00       0.00"
    "       0.00      45.49      48.99      73.99      64.96"
    "      74.40      88.64      52.29      64.11\n"
    + " MEDIA              0.00       0.00       0.00       0.00"
    "       0.00      12.73      37.14      42.93      46.42"
    "      47.52      48.47      41.34      39.51\n"
)

# Dataset 2: single series, two patamares — tests NaN/absent series fill
_MOCK_BLOCK_2023_SINGLE = (
    "     ANO: 2023\n"
    + _SEP
    + "     1    1         10.00      11.00      12.00      13.00"
    "      14.00      15.00      16.00      17.00      18.00"
    "      19.00      20.00      21.00      15.50\n"
    + "          2         20.00      22.00      24.00      26.00"
    "      28.00      30.00      32.00      34.00      36.00"
    "      38.00      40.00      42.00      31.00\n"
    + " MEDIA             15.00      16.50      18.00      19.50"
    "      21.00      22.50      24.00      25.50      27.00"
    "      28.50      30.00      31.50      23.25\n"
)

# Dataset 3: three series, two patamares — more carry-forward rows per series
_MOCK_BLOCK_2022_THREE = (
    "     ANO: 2022\n"
    + _SEP
    + "     1    1          5.00       5.10       5.20       5.30"
    "       5.40       5.50       5.60       5.70       5.80"
    "       5.90       6.00       6.10       5.55\n"
    + "          2          6.00       6.10       6.20       6.30"
    "       6.40       6.50       6.60       6.70       6.80"
    "       6.90       7.00       7.10       6.55\n"
    + "     2    1         15.00      15.10      15.20      15.30"
    "      15.40      15.50      15.60      15.70      15.80"
    "      15.90      16.00      16.10      15.55\n"
    + "          2         16.00      16.10      16.20      16.30"
    "      16.40      16.50      16.60      16.70      16.80"
    "      16.90      17.00      17.10      16.55\n"
    + "     3    1         25.00      25.10      25.20      25.30"
    "      25.40      25.50      25.60      25.70      25.80"
    "      25.90      26.00      26.10      25.55\n"
    + "          2         26.00      26.10      26.20      26.30"
    "      26.40      26.50      26.60      26.70      26.80"
    "      26.90      27.00      27.10      26.55\n"
    + " MEDIA             15.33      15.43      15.53      15.63"
    "      15.73      15.83      15.93      16.03      16.13"
    "      16.23      16.33      16.43      15.88\n"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_stream(text: str) -> io.StringIO:
    return io.StringIO(text)


def _read_block(cls, text: str):
    """Instantiate *cls* and call read() on *text*."""
    blk = cls()
    stream = _make_stream(text)
    blk.read(stream)
    return blk


# ---------------------------------------------------------------------------
# Tests — basic read
# ---------------------------------------------------------------------------


class TestTabelaSeriePatamarAnualRead:
    def test_begins_pattern(self):
        assert CmargsAnosTSPA.begins("     ANO: 2024\n")

    def test_ends_pattern(self):
        assert CmargsAnosTSPA.ends(" MEDIA              0.00\n")

    def test_data_is_dataframe(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        assert isinstance(blk.data, pd.DataFrame)

    def test_dataframe_columns(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        assert list(blk.data.columns) == ["data", "patamar", "serie", "valor"]

    def test_dataframe_first_date(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        assert blk.data.iloc[0]["data"] == datetime(2024, 1, 1)

    def test_dataframe_row_count_two_series_three_pat(self):
        # 2 series × 3 patamares × 12 months = 72 rows
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        assert len(blk.data) == 72

    def test_first_value_serie1_pat1_jan(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        val = blk.data[
            (blk.data["serie"] == 1)
            & (blk.data["patamar"] == 1)
            & (blk.data["data"] == datetime(2024, 1, 1))
        ]["valor"].iloc[0]
        assert val == pytest.approx(0.0)

    def test_value_serie1_pat1_jun(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        val = blk.data[
            (blk.data["serie"] == 1)
            & (blk.data["patamar"] == 1)
            & (blk.data["data"] == datetime(2024, 6, 1))
        ]["valor"].iloc[0]
        assert val == pytest.approx(22.54, rel=1e-4)

    def test_value_serie2_pat3_dec(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        val = blk.data[
            (blk.data["serie"] == 2)
            & (blk.data["patamar"] == 3)
            & (blk.data["data"] == datetime(2024, 12, 1))
        ]["valor"].iloc[0]
        assert val == pytest.approx(52.29, rel=1e-4)

    def test_series_dtype_is_int64(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        assert blk.data["serie"].dtype == "int64"

    def test_patamar_dtype_is_int64(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        assert blk.data["patamar"].dtype == "int64"


# ---------------------------------------------------------------------------
# Tests — series carry-forward
# ---------------------------------------------------------------------------


class TestTabelaSeriePatamarAnualCarryForward:
    """
    The carry-forward contract: rows where the serie field is blank in the
    source file must inherit the previous explicit serie value.
    """

    def test_all_rows_have_valid_series(self):
        """No NaN or zero series values after parsing."""
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        assert blk.data["serie"].notna().all()
        assert (blk.data["serie"] > 0).all()

    def test_carry_forward_populates_patamar_rows(self):
        """
        Series 1 has three patamar rows; only the first row is explicit.
        After carry-forward all three must show serie=1.
        """
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        s1_rows = blk.data[blk.data["serie"] == 1]
        assert len(s1_rows) == 36  # 3 patamares × 12 months

    def test_carry_forward_with_three_series(self):
        """
        Three-series block: each series group has two patamar rows.
        All 6 groups must be correctly resolved.
        """
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2022_THREE)
        for s in [1, 2, 3]:
            count = len(blk.data[blk.data["serie"] == s])
            assert count == 24  # 2 patamares × 12 months

    def test_single_series_fill_default(self):
        """
        When only one series is present and it is always explicit,
        the carry-forward must not corrupt the series column.
        """
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2023_SINGLE)
        assert (blk.data["serie"] == 1).all()


# ---------------------------------------------------------------------------
# Tests — output identical to ValoresSeriePatamar (CmargsAnos)
# ---------------------------------------------------------------------------


class TestTabelaSeriePatamarAnualIdenticalToLegacy:
    """
    The central contract: CmargsAnosTSPA must produce a DataFrame that is
    element-for-element identical to what CmargsAnos (ValoresSeriePatamar)
    produces on the same input.
    """

    def test_identical_dataframe_two_series_three_pat(self):
        blk_new = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        blk_old = _read_block(CmargsAnos, _MOCK_BLOCK_2024)

        assert blk_new.data is not None
        assert blk_old.data is not None
        pd.testing.assert_frame_equal(blk_new.data, blk_old.data)

    def test_identical_dataframe_single_series(self):
        blk_new = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2023_SINGLE)
        blk_old = _read_block(CmargsAnos, _MOCK_BLOCK_2023_SINGLE)

        assert blk_new.data is not None
        assert blk_old.data is not None
        pd.testing.assert_frame_equal(blk_new.data, blk_old.data)

    def test_identical_dataframe_three_series(self):
        blk_new = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2022_THREE)
        blk_old = _read_block(CmargsAnos, _MOCK_BLOCK_2022_THREE)

        assert blk_new.data is not None
        assert blk_old.data is not None
        pd.testing.assert_frame_equal(blk_new.data, blk_old.data)

    def test_column_names_match_legacy(self):
        blk_new = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        blk_old = _read_block(CmargsAnos, _MOCK_BLOCK_2024)
        assert list(blk_new.data.columns) == list(blk_old.data.columns)

    def test_dtypes_match_legacy(self):
        blk_new = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        blk_old = _read_block(CmargsAnos, _MOCK_BLOCK_2024)
        assert dict(blk_new.data.dtypes) == dict(blk_old.data.dtypes)


# ---------------------------------------------------------------------------
# Tests — __eq__
# ---------------------------------------------------------------------------


class TestTabelaSeriePatamarAnualEq:
    def test_eq_same_data(self):
        b1 = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        b2 = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        assert b1 == b2

    def test_neq_different_data(self):
        b1 = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        b2 = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2022_THREE)
        assert b1 != b2

    def test_neq_different_type(self):
        b1 = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        assert b1 != "not a block"

    def test_eq_both_empty(self):
        b1 = CmargsAnosTSPA()
        b2 = CmargsAnosTSPA()
        # Both have data=None; __eq__ returns True (neither is a DataFrame)
        assert b1 == b2

    def test_neq_one_empty(self):
        b1 = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        b2 = CmargsAnosTSPA()
        assert b1 != b2


# ---------------------------------------------------------------------------
# Tests — write round-trip
# ---------------------------------------------------------------------------


class TestTabelaSeriePatamarAnualWrite:
    def test_write_returns_true(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        out = io.StringIO()
        assert blk.write(out) is True

    def test_write_empty_returns_false(self):
        blk = CmargsAnosTSPA()
        out = io.StringIO()
        assert blk.write(out) is False

    def test_write_contains_ano_header(self):
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        out = io.StringIO()
        blk.write(out)
        assert "ANO: 2024" in out.getvalue()

    def test_write_round_trip_parses_identically(self):
        """
        Read -> write -> read must yield equal DataFrames.
        """
        blk1 = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)

        out = io.StringIO()
        blk1.write(out)
        reconstructed_text = out.getvalue()

        blk2 = _read_block(CmargsAnosTSPA, reconstructed_text)

        pd.testing.assert_frame_equal(blk1.data, blk2.data)

    def test_write_blanks_carry_forward_rows(self):
        """
        In the written output, rows that continue a series group
        (patamar > first) must have a blank serie field, not a repeated
        numeric value.
        """
        blk = _read_block(CmargsAnosTSPA, _MOCK_BLOCK_2024)
        out = io.StringIO()
        blk.write(out)
        lines = out.getvalue().splitlines()
        # Skip header (ANO line) and separator line; get data lines only.
        data_lines = [
            ln for ln in lines if ln and "ANO:" not in ln and "PAT" not in ln
        ]
        # Lines at index 1, 2 (patamar 2,3 of series 1) must have blank
        # serie field (columns 2..5).
        col_def = CmargsAnosTSPA.COLUMNS[0]
        start = col_def.field.starting_position
        width = col_def.field.size
        assert data_lines[1][start : start + width].strip() == ""
        assert data_lines[2][start : start + width].strip() == ""
        # Line at index 3 (first patamar of series 2) must be non-blank.
        assert data_lines[3][start : start + width].strip() != ""


# ---------------------------------------------------------------------------
# Tests — empty / edge cases
# ---------------------------------------------------------------------------


class TestTabelaSeriePatamarAnualEdgeCases:
    def test_empty_block_data_is_empty_dataframe(self):
        """
        A block whose ANO section has zero data rows should produce an
        empty DataFrame with the correct columns.
        """
        empty_block = (
            "     ANO: 2024\n"
            + _SEP
            + " MEDIA              0.00       0.00       0.00       0.00"
            "       0.00       0.00       0.00       0.00       0.00"
            "       0.00       0.00       0.00       0.00\n"
        )
        blk = _read_block(CmargsAnosTSPA, empty_block)
        assert isinstance(blk.data, pd.DataFrame)
        assert len(blk.data) == 0

    def test_columns_class_attribute_not_shared(self):
        """
        COLUMNS must be a class attribute of the subclass, not inherited
        from TabelaSeriePatamarAnual's empty list.
        """
        # 1 serie + 1 patamar + 12 months = 14 columns
        assert len(CmargsAnosTSPA.COLUMNS) == 14
        assert len(TabelaSeriePatamarAnual.COLUMNS) == 0

    def test_begin_pattern_is_ano(self):
        assert TabelaSeriePatamarAnual.BEGIN_PATTERN == "     ANO: "

    def test_end_pattern_has_leading_space(self):
        # END_PATTERN must be " MEDIA" (leading space) to avoid matching
        # the column-header line that contains "MEDIA " (trailing space).
        assert TabelaSeriePatamarAnual.END_PATTERN == " MEDIA"
        assert not TabelaSeriePatamarAnual.END_PATTERN.startswith("MEDIA")
