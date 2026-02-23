"""
Unit tests for TabelaSerieAnual.

A concrete subclass (EarmsAnosTSA) is defined here with the same field
layout as EarmsAnos so we can compare DataFrames produced by both classes
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
from inewave.nwlistop.modelos.blocos.tabela_serie_anual import (
    TabelaSerieAnual,
)
from inewave.nwlistop.modelos.earmf import EarmsAnos

# ---------------------------------------------------------------------------
# Concrete test subclass — same field layout as EarmsAnos
# ---------------------------------------------------------------------------

_FLOAT_FIELDS = [FloatField(8, 8 + 9 * i, 1) for i in range(len(MESES_DF))]

EARMSANOS_COLUMNS = [
    ColumnDef("serie", IntegerField(4, 2)),
] + [ColumnDef(MESES_DF[i], _FLOAT_FIELDS[i]) for i in range(len(MESES_DF))]


class EarmsAnosTSA(TabelaSerieAnual):
    """Test subclass mirroring EarmsAnos field layout."""

    __slots__: list = []

    COLUMNS = EARMSANOS_COLUMNS


# ---------------------------------------------------------------------------
# Minimal mock data — two series, two blocks, plus a MEDIA terminator
# ---------------------------------------------------------------------------

_SEP = (
    "           1        2        3        4        5        6"
    "        7        8        9       10       11       12      MEDIA \n"
)

_MOCK_BLOCK_2021 = (
    "     ANO: 2021\n"
    + _SEP
    + "     1   10028.   12548.   15830.   19790.   21654.   22386."
    "   22792.   23049.   20555.   15696.   17252.   23628.   18767.\n"
    + "     2   15514.   19228.   26832.   28490.   30688.   31722."
    "   32475.   32999.   32379.   32997.   35546.   41304.   30014.\n"
    + "MEDIA    12771.   15888.   21331.   24140.   26171.   27054."
    "   27634.   28024.   26467.   24347.   26399.   32466.\n"
)

_MOCK_BLOCK_2022 = (
    "     ANO: 2022\n"
    + _SEP
    + "     1    9000.    9100.    9200.    9300.    9400.    9500."
    "    9600.    9700.    9800.    9900.   10000.   10100.    9550.\n"
    + "MEDIA     9000.    9100.    9200.    9300.    9400.    9500."
    "    9600.    9700.    9800.    9900.   10000.   10100.\n"
)

# Third dataset: year 2019, four series, wide value range (small values near
# the minimum reservoir floor mixed with very large values near capacity).
# This exercises the parser across a larger series count than _MOCK_BLOCK_2021
# (4 vs 2) and across a broader numeric range (400–98000).
_MOCK_BLOCK_2019 = (
    "     ANO: 2019\n"
    + _SEP
    + "     1     400.     520.    1830.    4950.    8760.   12340."
    "   18200.   23050.   17600.    9320.    5140.    2870.    8748.\n"
    + "     2   51200.   63800.   74500.   82100.   89600.   93200."
    "   96700.   97800.   98000.   95400.   87300.   72100.   83475.\n"
    + "     3   25600.   31200.   39800.   47300.   53700.   59100."
    "   63400.   66200.   61500.   52800.   43900.   35700.   48358.\n"
    + "     4    1200.    1580.    2100.    3400.    4900.    6700."
    "    8300.    9100.    7200.    4600.    2900.    1500.    4465.\n"
    + "MEDIA   19600.   24275.   29558.   34438.   39240.   42835."
    "   46650.   49038.   46075.   40530.   34810.   28043.\n"
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


class TestTabelaSerieAnualRead:
    def test_begins_pattern(self):
        assert EarmsAnosTSA.begins("     ANO: 2021\n")

    def test_ends_pattern(self):
        assert EarmsAnosTSA.ends("MEDIA    12771.   15888.   21331.   24140.\n")

    def test_data_is_dataframe(self):
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        assert isinstance(blk.data, pd.DataFrame)

    def test_dataframe_columns(self):
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        assert list(blk.data.columns) == ["data", "serie", "valor"]

    def test_dataframe_first_date(self):
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        assert blk.data.iloc[0]["data"] == datetime(2021, 1, 1)

    def test_dataframe_row_count_two_series(self):
        # 2 series × 12 months = 24 rows
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        assert len(blk.data) == 24

    def test_first_value_matches_mock(self):
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        # First row: serie=1, January 2021 → 10028.0
        jan_s1 = blk.data[
            (blk.data["serie"] == 1)
            & (blk.data["data"] == datetime(2021, 1, 1))
        ]["valor"].iloc[0]
        assert jan_s1 == pytest.approx(10028.0, rel=1e-3)

    def test_last_value_matches_mock(self):
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        # Last row: serie=2, December 2021 → 41304.0
        dec_s2 = blk.data[
            (blk.data["serie"] == 2)
            & (blk.data["data"] == datetime(2021, 12, 1))
        ]["valor"].iloc[0]
        assert dec_s2 == pytest.approx(41304.0, rel=1e-3)

    def test_series_dtype_is_int64(self):
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        assert blk.data["serie"].dtype == "int64"

    def test_single_series_nan_replaced_by_one(self):
        """
        When a file has only one series and no series column is present,
        NaN must be replaced with 1 — identical to ValoresSerie behaviour.
        """
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2022)
        assert (blk.data["serie"] == 1).all()


# ---------------------------------------------------------------------------
# Tests — output identical to ValoresSerie
# ---------------------------------------------------------------------------


class TestTabelaSerieAnualIdenticalToValoresSerie:
    """
    The central contract: EarmsAnosTSA must produce a DataFrame that is
    element-for-element identical to what EarmsAnos (ValoresSerie) produces
    on the same input.
    """

    def test_identical_dataframe_two_series(self):
        blk_new = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        blk_old = _read_block(EarmsAnos, _MOCK_BLOCK_2021)

        assert blk_new.data is not None
        assert blk_old.data is not None
        pd.testing.assert_frame_equal(blk_new.data, blk_old.data)

    def test_identical_dataframe_single_series(self):
        blk_new = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2022)
        blk_old = _read_block(EarmsAnos, _MOCK_BLOCK_2022)

        assert blk_new.data is not None
        assert blk_old.data is not None
        pd.testing.assert_frame_equal(blk_new.data, blk_old.data)

    def test_identical_dataframe_four_series_wide_range(self):
        """
        Four series, year 2019, values spanning 400–98000.
        Exercises a larger series count and a much wider numeric range
        than the other two datasets.
        """
        blk_new = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2019)
        blk_old = _read_block(EarmsAnos, _MOCK_BLOCK_2019)

        assert blk_new.data is not None
        assert blk_old.data is not None
        pd.testing.assert_frame_equal(blk_new.data, blk_old.data)

    def test_column_names_match(self):
        blk_new = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        blk_old = _read_block(EarmsAnos, _MOCK_BLOCK_2021)
        assert list(blk_new.data.columns) == list(blk_old.data.columns)

    def test_dtypes_match(self):
        blk_new = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        blk_old = _read_block(EarmsAnos, _MOCK_BLOCK_2021)
        assert dict(blk_new.data.dtypes) == dict(blk_old.data.dtypes)


# ---------------------------------------------------------------------------
# Tests — __eq__
# ---------------------------------------------------------------------------


class TestTabelaSerieAnualEq:
    def test_eq_same_data(self):
        b1 = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        b2 = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        assert b1 == b2

    def test_neq_different_data(self):
        b1 = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        b2 = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2022)
        assert b1 != b2

    def test_neq_different_type(self):
        b1 = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        assert b1 != "not a block"

    def test_eq_both_empty(self):
        b1 = EarmsAnosTSA()
        b2 = EarmsAnosTSA()
        # Both have data=None; __eq__ returns True (neither is a DataFrame)
        assert b1 == b2

    def test_neq_one_empty(self):
        b1 = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        b2 = EarmsAnosTSA()
        assert b1 != b2


# ---------------------------------------------------------------------------
# Tests — write round-trip
# ---------------------------------------------------------------------------


class TestTabelaSerieAnualWrite:
    def test_write_returns_true(self):
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        out = io.StringIO()
        assert blk.write(out) is True

    def test_write_empty_returns_false(self):
        blk = EarmsAnosTSA()
        out = io.StringIO()
        assert blk.write(out) is False

    def test_write_contains_ano_header(self):
        blk = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)
        out = io.StringIO()
        blk.write(out)
        assert "ANO: 2021" in out.getvalue()

    def test_write_round_trip_parses_identically(self):
        """
        Read → write → read must yield equal DataFrames.
        """
        blk1 = _read_block(EarmsAnosTSA, _MOCK_BLOCK_2021)

        out = io.StringIO()
        blk1.write(out)
        reconstructed_text = out.getvalue()

        blk2 = _read_block(EarmsAnosTSA, reconstructed_text)

        pd.testing.assert_frame_equal(blk1.data, blk2.data)


# ---------------------------------------------------------------------------
# Tests — empty / edge cases
# ---------------------------------------------------------------------------


class TestTabelaSerieAnualEdgeCases:
    def test_empty_block_data_is_empty_dataframe(self):
        """
        A block whose ANO section has zero data rows should produce an
        empty DataFrame with the correct columns.
        """
        empty_block = (
            "     ANO: 2021\n"
            + _SEP
            + "MEDIA     0.0      0.0      0.0      0.0      0.0      0.0"
            "      0.0      0.0      0.0      0.0      0.0      0.0\n"
        )
        blk = _read_block(EarmsAnosTSA, empty_block)
        # No data rows → data must be an empty DataFrame (not None)
        assert isinstance(blk.data, pd.DataFrame)
        assert len(blk.data) == 0

    def test_columns_class_attribute_not_shared(self):
        """
        COLUMNS must be a class attribute of the subclass, not inherited
        from TabelaSerieAnual's empty list.
        """
        assert len(EarmsAnosTSA.COLUMNS) == 13  # 1 serie + 12 months
        assert len(TabelaSerieAnual.COLUMNS) == 0
