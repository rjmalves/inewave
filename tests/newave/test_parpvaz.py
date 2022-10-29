from inewave.newave.modelos.parpvaz import (
    BlocoSerieVazoesUHE,
    BlocoCorrelVazoesUHE,
    BlocoCorrelParcialVazoesUHE,
    BlocoOrdemModeloUHE,
    BlocoCoeficientesModeloUHE,
    BlocoSerieRuidosUHE,
    BlocoCorrelRuidosUHE,
    BlocoCorrelEspacialAnualMensalUHE,
)

from inewave.newave import PARpvaz


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.parpvaz import (
    MockSeriesVazoesPARpvaz,
    MockCorrelogramoSerieVazoesPARpvaz,
    MockCorrelogramoParcialSerieVazoesPARpvaz,
    MockOrdemOriginalModeloPARpvaz,
    MockCoeficientesModeloPARpvaz,
    MockSerieRuidosPARpvaz,
    MockCorrelogramoSerieRuidosPARpvaz,
    MockCorrelacaoEspacialPARpvaz,
    MockPARpvaz,
)


def test_series_vazoes_uhe():

    m: MagicMock = mock_open(read_data="".join(MockSeriesVazoesPARpvaz))
    b = BlocoSerieVazoesUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 90
    assert b.data.shape[1] == 15
    assert b.data.iloc[0, 3] == 302.0
    assert b.data.iloc[-1, -1] == 176.0


def test_correlacao_series_vazoes_uhe():

    m: MagicMock = mock_open(
        read_data="".join(MockCorrelogramoSerieVazoesPARpvaz)
    )
    b = BlocoCorrelVazoesUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12
    assert b.data.shape[1] == 12
    assert b.data.iloc[0, 1] == 0.45003
    assert b.data.iloc[-1, -1] == 0.2489


def test_correlacao_parcial_series_vazoes_uhe():

    m: MagicMock = mock_open(
        read_data="".join(MockCorrelogramoParcialSerieVazoesPARpvaz)
    )
    b = BlocoCorrelParcialVazoesUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12
    assert b.data.shape[1] == 12
    assert b.data.iloc[0, 1] == 0.45003
    assert b.data.iloc[-1, -1] == 0.00987


def test_ordem_modelo_uhe():

    m: MagicMock = mock_open(read_data="".join(MockOrdemOriginalModeloPARpvaz))
    b = BlocoOrdemModeloUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 1
    assert b.data.shape[1] == 14
    assert b.data.iloc[0, 2] == 6
    assert b.data.iloc[-1, -1] == 6


def test_coeficientes_modelo_uhe():

    m: MagicMock = mock_open(read_data="".join(MockCoeficientesModeloPARpvaz))
    b = BlocoCoeficientesModeloUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)
    print(b.data)
    assert b.data.shape[0] == 1
    assert b.data.shape[1] == 24
    assert b.data.loc[0, "Psi 1"] == 0.450
    assert b.data.loc[0, "Psi Norm 1"] == 0.727
    assert b.data.loc[0, "Psi A"] == 0.0
    assert b.data.loc[0, "Psi Norm A"] == 0.0


def test_serie_ruidos_uhe():

    m: MagicMock = mock_open(read_data="".join(MockSerieRuidosPARpvaz))
    b = BlocoSerieRuidosUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 90
    assert b.data.shape[1] == 14
    assert b.data.iloc[0, 1] == 0.0
    assert b.data.iloc[-1, -1] == -0.0752


def test_correl_serie_ruidos_uhe():

    m: MagicMock = mock_open(
        read_data="".join(MockCorrelogramoSerieRuidosPARpvaz)
    )
    b = BlocoCorrelRuidosUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12
    assert b.data.shape[1] == 12
    assert b.data.iloc[0, 1] == -0.06325
    assert b.data.iloc[-1, -1] == 0.00761


def test_correl_espacial_anual_mensal():

    m: MagicMock = mock_open(read_data="".join(MockCorrelacaoEspacialPARpvaz))
    b = BlocoCorrelEspacialAnualMensalUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 17
    assert b.data.shape[1] == 15
    assert b.data.iloc[0, 2] == 0.55
    assert b.data.iloc[-1, -1] == 0.52


def test_atributos_encontrados_parpvaz():
    m: MagicMock = mock_open(read_data="".join(MockPARpvaz))
    with patch("builtins.open", m):
        parp = PARpvaz.le_arquivo("")
        assert parp.series_vazoes_uhe is not None
        assert parp.correlacao_series_vazoes_uhe is not None
        assert parp.correlacao_parcial_series_vazoes_uhe is not None
        assert parp.ordem_original_modelo is not None
        assert parp.ordem_final_modelo is not None
        assert parp.coeficientes is not None
        assert parp.series_ruido_uhe is not None
        assert parp.correlacao_series_ruidos_uhe is not None
        assert parp.correlacao_espacial_anual_mensal is not None


def test_atributos_nao_encontrados_parpvaz():
    m: MagicMock = mock_open(read_data="".join(MockSerieRuidosPARpvaz))
    with patch("builtins.open", m):
        parp = PARpvaz.le_arquivo("")
        assert parp.series_vazoes_uhe is None
        assert parp.correlacao_series_vazoes_uhe is None
        assert parp.correlacao_parcial_series_vazoes_uhe is None
        assert parp.ordem_original_modelo is None
        assert parp.ordem_final_modelo is None
        assert parp.coeficientes is None
        assert parp.series_ruido_uhe is None
        assert parp.correlacao_series_ruidos_uhe is None
        assert parp.correlacao_espacial_anual_mensal is None


def test_eq_parpvaz():
    m: MagicMock = mock_open(read_data="".join(MockPARpvaz))
    with patch("builtins.open", m):
        parp1 = PARpvaz.le_arquivo("")
        parp2 = PARpvaz.le_arquivo("")
        assert parp1 == parp2


def test_neq_parpvaz():
    m: MagicMock = mock_open(read_data="".join(MockPARpvaz))
    with patch("builtins.open", m):
        parp1 = PARpvaz.le_arquivo("")
        parp2 = PARpvaz.le_arquivo("")
        parp2.series_vazoes_uhe.iloc[0, 0] = -1
        assert parp1 != parp2
