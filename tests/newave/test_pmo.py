from inewave.newave.modelos.pmo import (
    BlocoConvergenciaPMO,
    BlocoEafPastTendenciaHidrolPMO,
    BlocoEafPastCfugaMedioPMO,
    BlocoConfiguracoesExpansaoPMO,
    BlocoMARSPMO,
    BlocoRiscoDeficitENSPMO,
    BlocoCustoOperacaoPMO,
    BlocoCustoOperacaoTotalPMO,
    BlocoProdutibilidadesConfiguracaoPMO,
    BlocoEnergiaArmazenadaInicialPMO,
    BlocoVolumeArmazenadoInicialPMO,
)

from inewave.newave import Pmo
from datetime import datetime

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.pmo import MockBlocoEafPastTendenciaHidrolPMO
from tests.mocks.arquivos.pmo import MockBlocoEafPastCfugaMedioPMO
from tests.mocks.arquivos.pmo import MockBlocoConvergenciaPMO
from tests.mocks.arquivos.pmo import (
    MockBlocoConfiguracoesExpansaoEntradaReservatorioPMO,
)
from tests.mocks.arquivos.pmo import MockBlocoProdutibilidadesPMO
from tests.mocks.arquivos.pmo import MockBlocoMARSPMOInicial
from tests.mocks.arquivos.pmo import MockBlocoMARSPMOFinal
from tests.mocks.arquivos.pmo import MockBlocoRiscoDeficitENSPMO
from tests.mocks.arquivos.pmo import MockBlocoCustoOperacaoPMO
from tests.mocks.arquivos.pmo import MockBlocoCustoOperacaoTotalPMO
from tests.mocks.arquivos.pmo import MockBlocoEnergiaArmazenadaInicialPMO
from tests.mocks.arquivos.pmo import MockBlocoVolumeArmazenadoInicialPMO
from tests.mocks.arquivos.pmo import MockPMO

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_eafpast_tendencia_hidrologica():
    m: MagicMock = mock_open(
        read_data="".join(MockBlocoEafPastTendenciaHidrolPMO)
    )
    b = BlocoEafPastTendenciaHidrolPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 144
    assert b.data.shape[1] == 3
    assert b.data.iloc[0, 1] == 1
    assert b.data.iloc[0, 2] == 7196.96
    assert b.data.iloc[-1, -1] == 409.13


def test_eafpast_cfuga_medio():
    m: MagicMock = mock_open(read_data="".join(MockBlocoEafPastCfugaMedioPMO))
    b = BlocoEafPastCfugaMedioPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 144
    assert b.data.shape[1] == 3
    assert b.data.iloc[0, 1] == 1
    assert b.data.iloc[0, 2] == 7196.96
    assert b.data.iloc[-1, -1] == 409.13


def test_energia_armazenada_inicial():
    m: MagicMock = mock_open(
        read_data="".join(MockBlocoEnergiaArmazenadaInicialPMO)
    )
    b = BlocoEnergiaArmazenadaInicialPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12
    assert b.data.shape[1] == 3
    assert b.data.iloc[0, 0] == "SUDESTE"
    assert b.data.iloc[0, 1] == 16191.0
    assert b.data.iloc[0, 2] == 31.8
    assert b.data.iloc[-1, -1] == 34.3


def test_volume_armazenado_inicial():
    m: MagicMock = mock_open(
        read_data="".join(MockBlocoVolumeArmazenadoInicialPMO)
    )
    b = BlocoVolumeArmazenadoInicialPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 164
    assert b.data.shape[1] == 4
    assert b.data.iloc[1, 0] == 20
    assert b.data.iloc[1, 1] == "BATALHA"
    assert b.data.iloc[1, 2] == 414.9
    assert b.data.iloc[1, 3] == 30.7
    assert b.data.iloc[-1, -1] == 0.0


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

    assert b.data.iloc[0, 0] == datetime(2021, 1, 1)
    assert b.data.iloc[-1, 0] == datetime(2030, 12, 1)
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

    assert b.data.shape[0] == 20
    assert b.data.iloc[0, 0] == 2021
    assert b.data.iloc[0, 1] == "SUDESTE"
    assert b.data.iloc[0, 2] == 0.0
    assert b.data.iloc[0, 3] == 0.0


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


def test_leitura_produtibilidades():
    m: MagicMock = mock_open(read_data="".join(MockBlocoProdutibilidadesPMO))
    b = BlocoProdutibilidadesConfiguracaoPMO()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert len(list(b.data.index)) == 1312
    assert b.data.iloc[1, 1] == 1
    assert b.data.iloc[1, 2] == 0.4483
    assert b.data.iloc[1, 3] == 0.4334
    assert b.data.iloc[1, 4] == 0.4005
    assert b.data.iloc[1, 5] == 0.4625
    assert b.data.iloc[1, 6] == 0.4886
    assert b.data.iloc[1, 7] == 2.2083
    assert b.data.iloc[1, 8] == 2.1858
    assert b.data.iloc[1, 9] == 2.2292
    assert b.data.iloc[1, 10] == 2.1382
    assert b.data.iloc[1, 11] == 2.2292
    assert b.data.iloc[1, 12] == 2.2697
    assert b.data.iloc[1, 13] == 2.1382
    assert b.data.iloc[1, 14] == 2.2292
    assert b.data.iloc[1, 15] == 2.2697


def test_atributos_encontrados_pmo():
    m: MagicMock = mock_open(read_data="".join(MockPMO))
    with patch("builtins.open", m):
        pmo = Pmo.read(ARQ_TESTE)
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
        assert pmo.produtibilidades_equivalentes is not None
        assert pmo.energia_armazenada_inicial is not None
        assert pmo.volume_armazenado_inicial is not None


def test_atributos_nao_encontrados_pmo():
    m: MagicMock = mock_open(read_data="".join(MockBlocoConvergenciaPMO))
    with patch("builtins.open", m):
        pmo = Pmo.read(ARQ_TESTE)
        assert pmo.convergencia is not None
        assert pmo.custo_operacao_series_simuladas is None
        assert pmo.custo_operacao_total is None
        assert pmo.desvio_custo_operacao_total is None
        assert pmo.produtibilidades_equivalentes is None
        assert pmo.energia_armazenada_inicial is None
        assert pmo.volume_armazenado_inicial is None


def test_eq_pmo():
    m: MagicMock = mock_open(read_data="".join(MockPMO))
    with patch("builtins.open", m):
        pmo1 = Pmo.read(ARQ_TESTE)
        pmo2 = Pmo.read(ARQ_TESTE)
        assert pmo1 == pmo2


def test_neq_pmo():
    m: MagicMock = mock_open(read_data="".join(MockPMO))
    with patch("builtins.open", m):
        pmo1 = Pmo.read(ARQ_TESTE)
        pmo2 = Pmo.read(ARQ_TESTE)
        pmo2.configuracoes_alteracao_potencia
        assert pmo1 == pmo2
