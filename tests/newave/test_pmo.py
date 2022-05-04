from inewave.newave.modelos.pmo import (
    BlocoConvergenciaPMO,
    BlocoEafPastTendenciaHidrolPMO,
    BlocoEafPastCfugaMedioPMO,
    BlocoConfiguracoesExpansaoPMO,
    BlocoMARSPMO,
    BlocoRiscoDeficitENSPMO,
    BlocoCustoOperacaoPMO,
    BlocoCustoOperacaoTotalPMO,
)

from inewave.newave import PMO


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.pmo import MockBlocoEafPastTendenciaHidrolPMO
from tests.mocks.arquivos.pmo import MockBlocoEafPastCfugaMedioPMO
from tests.mocks.arquivos.pmo import MockBlocoConvergenciaPMO
from tests.mocks.arquivos.pmo import (
    MockBlocoConfiguracoesExpansaoEntradaReservatorioPMO,
)
from tests.mocks.arquivos.pmo import MockBlocoMARSPMOInicial
from tests.mocks.arquivos.pmo import MockBlocoMARSPMOFinal
from tests.mocks.arquivos.pmo import MockBlocoRiscoDeficitENSPMO
from tests.mocks.arquivos.pmo import MockBlocoCustoOperacaoPMO
from tests.mocks.arquivos.pmo import MockBlocoCustoOperacaoTotalPMO
from tests.mocks.arquivos.pmo import MockPMO


def test_eafpast_tendencia_hidrologica():

    m: MagicMock = mock_open(
        read_data="".join(MockBlocoEafPastTendenciaHidrolPMO)
    )
    b = BlocoEafPastTendenciaHidrolPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12
    assert b.data.shape[1] == 13
    assert b.data.iloc[0, 1] == 7196.96
    assert b.data.iloc[-1, -1] == 409.13


def test_eafpast_cfuga_medio():

    m: MagicMock = mock_open(read_data="".join(MockBlocoEafPastCfugaMedioPMO))
    b = BlocoEafPastCfugaMedioPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12
    assert b.data.shape[1] == 13
    assert b.data.iloc[0, 1] == 7196.96
    assert b.data.iloc[-1, -1] == 409.13


def test_convergencia():

    m: MagicMock = mock_open(read_data="".join(MockBlocoConvergenciaPMO))
    b = BlocoConvergenciaPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert len(list(b.data.index)) == 135


def test_leitura_configs():
    m: MagicMock = mock_open(
        read_data="".join(MockBlocoConfiguracoesExpansaoEntradaReservatorioPMO)
    )
    b = BlocoConfiguracoesExpansaoPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 2021
    assert b.data.iloc[-1, 0] == 2030
    assert b.data.iloc[0, 1] == 1
    assert b.data.iloc[-1, -1] == 60


def test_leitura_retas_perdas_inicial():
    m: MagicMock = mock_open(read_data="".join(MockBlocoMARSPMOInicial))
    b = BlocoMARSPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 2] == 0.074069


def test_leitura_retas_perdas_final():
    m: MagicMock = mock_open(read_data="".join(MockBlocoMARSPMOFinal))
    b = BlocoMARSPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 2] == 0.074069


def test_leitura_ens_deficit():
    m: MagicMock = mock_open(read_data="".join(MockBlocoRiscoDeficitENSPMO))
    b = BlocoRiscoDeficitENSPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert len(list(b.data.index)) == 5
    assert b.data.iloc[4, 1] == 0.0
    assert b.data.iloc[4, 2] == 0.0
    assert b.data.iloc[4, 3] == 0.0
    assert b.data.iloc[4, 4] == 0.0


def test_leitura_tabelas_custos():
    m: MagicMock = mock_open(read_data="".join(MockBlocoCustoOperacaoPMO))
    b = BlocoCustoOperacaoPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 1] == 21887.91


def test_leitura_custo_total():
    m: MagicMock = mock_open(read_data="".join(MockBlocoCustoOperacaoTotalPMO))
    b = BlocoCustoOperacaoTotalPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data[0] == 22323.17
    assert b.data[1] == 107.00


def test_atributos_encontrados_pmo():
    m: MagicMock = mock_open(read_data="".join(MockPMO))
    with patch("builtins.open", m):
        pmo = PMO.le_arquivo("")
        assert pmo.eafpast_tendencia_hidrologica is not None
        assert pmo.eafpast_cfuga_medio is not None
        assert pmo.convergencia is not None
        assert pmo.configuracoes_alteracao_potencia is not None
        assert pmo.configuracoes_entrada_reservatorio is not None
        assert pmo.configuracoes_qualquer_modificacao is not None
        assert pmo.retas_perdas_engolimento(1) is not None
        assert pmo.retas_perdas_engolimento(2) is not None
        assert pmo.risco_deficit_ens is not None
        assert pmo.custo_operacao_series_simuladas is not None
        assert pmo.custo_operacao_referenciado_primeiro_mes is not None
        assert pmo.valor_esperado_periodo_estudo is not None
        assert pmo.custo_operacao_total is not None
        assert pmo.desvio_custo_operacao_total is not None


def test_atributos_nao_encontrados_pmo():
    m: MagicMock = mock_open(read_data="".join(MockBlocoConvergenciaPMO))
    with patch("builtins.open", m):
        pmo = PMO.le_arquivo("")
        assert pmo.convergencia is not None
        assert pmo.custo_operacao_series_simuladas is None
        assert pmo.custo_operacao_total is None
        assert pmo.desvio_custo_operacao_total is None


def test_eq_pmo():
    m: MagicMock = mock_open(read_data="".join(MockPMO))
    with patch("builtins.open", m):
        pmo1 = PMO.le_arquivo("")
        pmo2 = PMO.le_arquivo("")
        assert pmo1 == pmo2


def test_neq_pmo():
    m: MagicMock = mock_open(read_data="".join(MockPMO))
    with patch("builtins.open", m):
        pmo1 = PMO.le_arquivo("")
        pmo2 = PMO.le_arquivo("")
        pmo2.configuracoes_alteracao_potencia
        assert pmo1 == pmo2
