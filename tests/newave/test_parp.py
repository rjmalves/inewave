from inewave.newave.modelos.parp import (
    BlocoSerieEnergiaREE,
    BlocoCorrelEnergiasREE,
    BlocoCorrelParcialEnergiasREE,
    BlocoOrdemModeloREE,
    BlocoCoeficientesModeloREE,
    BlocoSerieRuidosREE,
    BlocoCorrelRuidosREE,
    BlocoSerieMediasREE,
    BlocoCorrelCruzadaMediaREE,
    BlocoCorrelEspacialAnualConfig,
    BlocoCorrelEspacialMensalConfig,
)

from inewave.newave import PARp


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.parp import (
    MockSeriesEnergiaPARp,
    MockCorrelacaoSeriesEnergiasREE,
    MockCorrelacaoParcialSeriesEnergiaREE,
    MockOrdemOriginalModeloREE,
    MockCoeficientesModeloREE,
    MockSerieRuidosREE,
    MockCorrelSerieRuidosREE,
    MockSerieMedia12MesesREE,
    MockCorrelCruzadaMedia12Meses,
    MockCorrelEspacialAnual,
    MockCorrelEspacialMensal,
    MockPARp,
)


def test_series_energia_ree():

    m: MagicMock = mock_open(read_data="".join(MockSeriesEnergiaPARp))
    b = BlocoSerieEnergiaREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 87
    assert b.data.shape[1] == 15
    assert b.data.iloc[0, 3] == 8536.82
    assert b.data.iloc[-1, -1] == 5616.44


def test_correlacao_series_energia_ree():

    m: MagicMock = mock_open(
        read_data="".join(MockCorrelacaoSeriesEnergiasREE)
    )
    b = BlocoCorrelEnergiasREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 120
    assert b.data.shape[1] == 12
    assert b.data.iloc[0, 1] == 0.28570
    assert b.data.iloc[-1, -1] == 0.04142


def test_correlacao_parcial_series_energia_ree():

    m: MagicMock = mock_open(
        read_data="".join(MockCorrelacaoParcialSeriesEnergiaREE)
    )
    b = BlocoCorrelParcialEnergiasREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 120
    assert b.data.shape[1] == 12
    assert b.data.iloc[0, 1] == 0.19220
    assert b.data.iloc[-1, -1] == -0.15513


def test_ordem_modelo_ree():

    m: MagicMock = mock_open(read_data="".join(MockOrdemOriginalModeloREE))
    b = BlocoOrdemModeloREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 10
    assert b.data.shape[1] == 14
    assert b.data.iloc[0, 2] == 1
    assert b.data.iloc[-1, -1] == 4


def test_coeficientes_modelo_ree():

    m: MagicMock = mock_open(read_data="".join(MockCoeficientesModeloREE))
    b = BlocoCoeficientesModeloREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 1
    assert b.data.shape[1] == 24
    assert b.data.loc[0, "Psi 1"] == 0.207
    assert b.data.loc[0, "Psi Norm 1"] == 0.263
    assert b.data.loc[0, "Psi A"] == 0.177
    assert b.data.loc[0, "Psi Norm A"] == 0.485


def test_serie_ruidos_ree():

    m: MagicMock = mock_open(read_data="".join(MockSerieRuidosREE))
    b = BlocoSerieRuidosREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 87
    assert b.data.shape[1] == 14
    assert b.data.iloc[0, 1] == 0.0
    assert b.data.iloc[-1, -1] == -0.152


def test_correl_serie_ruidos_ree():

    m: MagicMock = mock_open(read_data="".join(MockCorrelSerieRuidosREE))
    b = BlocoCorrelRuidosREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 120
    assert b.data.shape[1] == 12
    assert b.data.iloc[0, 1] == -0.05921
    assert b.data.iloc[-1, -1] == -0.08159


def test_serie_media_12_meses_ree():

    m: MagicMock = mock_open(read_data="".join(MockSerieMedia12MesesREE))
    b = BlocoSerieMediasREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 87
    assert b.data.shape[1] == 14
    assert b.data.iloc[0, 1] == 0.0000
    assert b.data.iloc[-1, -1] == 3136.70


def test_correl_cruzada_media_12_meses_ree():

    m: MagicMock = mock_open(read_data="".join(MockCorrelCruzadaMedia12Meses))
    b = BlocoCorrelCruzadaMediaREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 120
    assert b.data.shape[1] == 13
    assert b.data.iloc[0, 1] == 0.26913
    assert b.data.iloc[-1, -1] == 0.76845


def test_correl_espacial_anual():

    m: MagicMock = mock_open(read_data="".join(MockCorrelEspacialAnual))
    b = BlocoCorrelEspacialAnualConfig()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12
    assert b.data.shape[1] == 14
    assert b.data.iloc[0, 2] == 1.000
    assert b.data.iloc[-1, -1] == 1.000


def test_correl_espacial_mensal():

    m: MagicMock = mock_open(read_data="".join(MockCorrelEspacialMensal))
    b = BlocoCorrelEspacialMensalConfig()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12
    assert b.data.shape[1] == 15
    assert b.data.iloc[0, 3] == 1.0000
    assert b.data.iloc[-1, -1] == 0.0671


def test_atributos_encontrados_parp():
    m: MagicMock = mock_open(read_data="".join(MockPARp))
    with patch("builtins.open", m):
        parp = PARp.le_arquivo("")
        assert parp.series_energia_ree is not None
        assert parp.correlacao_series_energia_ree is not None
        assert parp.correlacao_parcial_series_energia_ree is not None
        assert parp.ordem_original_modelo is not None
        assert parp.ordem_final_modelo is not None
        assert parp.coeficientes is not None
        assert parp.series_media_ree is not None
        assert parp.series_ruido_ree is not None
        assert parp.correlacao_series_ruidos_ree is not None
        assert parp.correlacao_cruzada_media_ree is not None
        assert parp.correlacao_espacial_anual is not None
        assert parp.correlacao_espacial_mensal is not None


def test_atributos_nao_encontrados_parp():
    m: MagicMock = mock_open(read_data="".join(MockSeriesEnergiaPARp))
    with patch("builtins.open", m):
        parp = PARp.le_arquivo("")
        assert parp.series_energia_ree is not None
        assert parp.correlacao_series_energia_ree is None
        assert parp.correlacao_parcial_series_energia_ree is None
        assert parp.ordem_original_modelo is None
        assert parp.ordem_final_modelo is None
        assert parp.coeficientes is None
        assert parp.series_media_ree is None
        assert parp.series_ruido_ree is None
        assert parp.correlacao_series_ruidos_ree is None
        assert parp.correlacao_cruzada_media_ree is None
        assert parp.correlacao_espacial_anual is None
        assert parp.correlacao_espacial_mensal is None


def test_eq_parp():
    m: MagicMock = mock_open(read_data="".join(MockPARp))
    with patch("builtins.open", m):
        parp1 = PARp.le_arquivo("")
        parp2 = PARp.le_arquivo("")
        assert parp1 == parp2


def test_neq_parp():
    m: MagicMock = mock_open(read_data="".join(MockPARp))
    with patch("builtins.open", m):
        parp1 = PARp.le_arquivo("")
        parp2 = PARp.le_arquivo("")
        parp2.series_energia_ree.iloc[0, 0] = -1
        assert parp1 != parp2
