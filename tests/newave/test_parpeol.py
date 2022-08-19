from inewave.newave.modelos.parpeol import (
    BlocoSerieVentosUEE,
    BlocoCorrelVentosUEE,
    BlocoSerieRuidosUEE,
    BlocoCorrelRuidosUEE,
    BlocoCorrelEspacialAnualConfig,
    BlocoCorrelEspacialMensalConfig,
)

from inewave.newave.parpeol import PARpeol


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.parpeol import (
    MockSeriesVentosUEE,
    MockCorrelacaoSeriesVentosUEE,
    MockSerieRuidosUEE,
    MockCorrelSerieRuidosUEE,
    MockCorrelEspacialAnual,
    MockCorrelEspacialMensal,
    MockPARpeol,
)


def test_series_ventos_uee():

    m: MagicMock = mock_open(read_data="".join(MockSeriesVentosUEE))
    b = BlocoSerieVentosUEE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 40
    assert b.data.shape[1] == 15
    assert b.data.iloc[0, 3] == 6.31
    assert b.data.iloc[-1, -1] == 6.93


def test_correlacao_series_ventos_uee():

    m: MagicMock = mock_open(read_data="".join(MockCorrelacaoSeriesVentosUEE))
    b = BlocoCorrelVentosUEE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 120
    assert b.data.shape[1] == 12
    assert b.data.iloc[0, 1] == -0.06591
    assert b.data.iloc[-1, -1] == 0.29579


def test_serie_ruidos_uee():

    m: MagicMock = mock_open(read_data="".join(MockSerieRuidosUEE))
    b = BlocoSerieRuidosUEE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 40
    assert b.data.shape[1] == 14
    assert b.data.iloc[0, 1] == 0.0
    assert b.data.iloc[-1, -1] == 0.497


def test_correl_serie_ruidos_uee():

    m: MagicMock = mock_open(read_data="".join(MockCorrelSerieRuidosUEE))
    b = BlocoCorrelRuidosUEE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 120
    assert b.data.shape[1] == 12
    assert b.data.iloc[0, 1] == 0.29579
    assert b.data.iloc[-1, -1] == 0.00582


def test_correl_espacial_anual():

    m: MagicMock = mock_open(read_data="".join(MockCorrelEspacialAnual))
    b = BlocoCorrelEspacialAnualConfig()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 2
    assert b.data.shape[1] == 16
    assert b.data.iloc[0, 2] == -0.2010
    assert b.data.iloc[-1, -1] == 1.000


def test_correl_espacial_mensal():

    m: MagicMock = mock_open(read_data="".join(MockCorrelEspacialMensal))
    b = BlocoCorrelEspacialMensalConfig()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 24
    assert b.data.shape[1] == 17
    assert b.data.iloc[0, 3] == -0.3616
    assert b.data.iloc[-1, -1] == 1.000


def test_atributos_encontrados_parpeol():
    m: MagicMock = mock_open(read_data="".join(MockPARpeol))
    with patch("builtins.open", m):
        parp = PARpeol.le_arquivo("")
        assert parp.series_ventos_uee is not None
        assert parp.correlacao_series_ventos_uee is not None
        assert parp.series_ruido_uee is not None
        assert parp.correlacao_series_ruidos_uee is not None
        assert parp.correlacao_espacial_anual is not None
        assert parp.correlacao_espacial_mensal is not None


def test_atributos_nao_encontrados_parp():
    m: MagicMock = mock_open(read_data="".join(""))
    with patch("builtins.open", m):
        parp = PARpeol.le_arquivo("")
        assert parp.series_ventos_uee is None
        assert parp.correlacao_series_ventos_uee is None
        assert parp.series_ruido_uee is None
        assert parp.correlacao_series_ruidos_uee is None
        assert parp.correlacao_espacial_anual is None
        assert parp.correlacao_espacial_mensal is None


def test_eq_parpeol():
    m: MagicMock = mock_open(read_data="".join(MockPARpeol))
    with patch("builtins.open", m):
        parp1 = PARpeol.le_arquivo("")
        parp2 = PARpeol.le_arquivo("")
        assert parp1 == parp2


def test_neq_parpeol():
    m: MagicMock = mock_open(read_data="".join(MockPARpeol))
    with patch("builtins.open", m):
        parp1 = PARpeol.le_arquivo("")
        parp2 = PARpeol.le_arquivo("")
        parp2.series_ventos_uee.iloc[0, 0] = -1
        assert parp1 != parp2
