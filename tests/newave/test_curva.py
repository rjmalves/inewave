# Rotinas de testes associadas ao arquivo curva.dat do NEWAVE
from inewave.newave.modelos.curva import (
    BlocoConfiguracoesPenalizacaoCurva,
    BlocoPenalidadesViolacaoREECurva,
    BlocoCurvaSegurancaREE,
    BlocoMaximoIteracoesProcessoIterativoEtapa2,
    BlocoIteracaoAPartirProcessoIterativoEtapa2,
    BlocoToleranciaProcessoIterativoEtapa2,
    BlocoImpressaoRelatorioProcessoIterativoEtapa2,
)

from inewave.newave import Curva

from datetime import datetime

import numpy as np
import pytest

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.curva import (
    MockBlockTipoPenalizacao,
    MockBlocoCustoPorSistema,
    MockBlocoCurvaSeguranca,
    MockMaximoIteracoesProcessoIterativoEtapa2,
    MockIteracaoAPartirProcessoIterativoEtapa2,
    MockToleranciaProcessoIterativoEtapa2,
    MockImpressaoRelatorioProcessoIterativoEtapa2,
    MockCurva,
    MockBlocoCurvaSegurancaComEspacos,
    MockCurvaComEspacos,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_configuracoes_penalizacao_curva():
    m: MagicMock = mock_open(read_data="".join(MockBlockTipoPenalizacao))
    b = BlocoConfiguracoesPenalizacaoCurva()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == [1, 11, 1]


def test_bloco_penalidades_ree():
    m: MagicMock = mock_open(read_data="".join(MockBlocoCustoPorSistema))
    b = BlocoPenalidadesViolacaoREECurva()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 1745.08


def test_bloco_curva_seguranca():
    m: MagicMock = mock_open(read_data="".join(MockBlocoCurvaSeguranca))
    b = BlocoCurvaSegurancaREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 10.0


def _valor_curva(df, codigo_ree: int, ano: int, mes: int) -> float:
    linha = df.loc[
        (df["codigo_ree"] == codigo_ree)
        & (df["data"] == datetime(year=ano, month=mes, day=1))
    ]
    assert len(linha) == 1
    return float(linha["valor"].iloc[0])


def test_bloco_curva_seguranca_linhas_com_espacos():
    m: MagicMock = mock_open(
        read_data="".join(MockBlocoCurvaSegurancaComEspacos)
    )
    b = BlocoCurvaSegurancaREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data["codigo_ree"].unique().tolist() == [1, 2, 12]
    assert len(b.data) == 3 * 2 * 12
    assert b.data["data"].min() == datetime(year=2026, month=1, day=1)
    # Meses anteriores ao início do estudo, em branco no arquivo
    assert b.data["valor"].isna().sum() == 3 * 10
    assert np.isnan(_valor_curva(b.data, 1, 2026, 10))
    assert _valor_curva(b.data, 1, 2026, 11) == 20.0
    assert _valor_curva(b.data, 1, 2027, 12) == 20.0
    assert _valor_curva(b.data, 2, 2026, 12) == 30.0
    assert _valor_curva(b.data, 12, 2027, 6) == 25.5


def test_bloco_curva_seguranca_ano_sem_meses_preenchidos():
    linhas = MockBlocoCurvaSeguranca[:5] + ["2022\n", "9999\n"]
    m: MagicMock = mock_open(read_data="".join(linhas))
    b = BlocoCurvaSegurancaREE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data["codigo_ree"].unique().tolist() == [1]
    assert len(b.data) == 2 * 12
    assert b.data["data"].max() == datetime(year=2022, month=12, day=1)
    assert b.data["valor"].isna().sum() == 12


def test_bloco_maximo_iteracoes():
    m: MagicMock = mock_open(
        read_data="".join(MockMaximoIteracoesProcessoIterativoEtapa2)
    )
    b = BlocoMaximoIteracoesProcessoIterativoEtapa2()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == 0


def test_bloco_iteracao_a_partir():
    m: MagicMock = mock_open(
        read_data="".join(MockIteracaoAPartirProcessoIterativoEtapa2)
    )
    b = BlocoIteracaoAPartirProcessoIterativoEtapa2()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == 10


def test_bloco_tolerancia_processo():
    m: MagicMock = mock_open(
        read_data="".join(MockToleranciaProcessoIterativoEtapa2)
    )
    b = BlocoToleranciaProcessoIterativoEtapa2()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == 0.01


def test_bloco_impressao_relatorio():
    m: MagicMock = mock_open(
        read_data="".join(MockImpressaoRelatorioProcessoIterativoEtapa2)
    )
    b = BlocoImpressaoRelatorioProcessoIterativoEtapa2()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == 0


def test_atributos_encontrados_curva():
    m: MagicMock = mock_open(read_data="".join(MockCurva))
    with patch("builtins.open", m):
        ad = Curva.read(ARQ_TESTE)
        assert ad.configuracoes_penalizacao != [None, None, None]
        assert ad.custos_penalidades is not None
        assert ad.curva_seguranca is not None
        assert ad.maximo_iteracoes_etapa2 is not None
        assert ad.iteracao_a_partir_etapa2 is not None
        assert ad.tolerancia_processo_etapa2 is not None
        assert ad.impressao_relatorio_etapa2 is not None


def test_atributos_curva_linhas_com_espacos():
    m: MagicMock = mock_open(read_data="".join(MockCurvaComEspacos))
    with patch("builtins.open", m):
        ad = Curva.read(ARQ_TESTE)
    assert ad.configuracoes_penalizacao == [1, 11, 1]
    assert ad.custos_penalidades["codigo_ree"].tolist() == [1, 2, 12]
    assert ad.custos_penalidades["penalidade"].tolist() == [5192.04] * 3
    assert ad.curva_seguranca["codigo_ree"].unique().tolist() == [1, 2, 12]
    assert ad.curva_seguranca["data"].min() == datetime(
        year=2026, month=1, day=1
    )
    assert _valor_curva(ad.curva_seguranca, 12, 2027, 6) == 25.5
    assert ad.maximo_iteracoes_etapa2 == 0
    assert ad.iteracao_a_partir_etapa2 == 10
    assert ad.tolerancia_processo_etapa2 == 0.01
    assert ad.impressao_relatorio_etapa2 == 0


def test_atributos_nao_encontrados_curva():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Curva.read(ARQ_TESTE)
        assert ad.configuracoes_penalizacao == [None, None, None]
        assert ad.custos_penalidades is None
        assert ad.curva_seguranca is None
        assert ad.maximo_iteracoes_etapa2 is None
        assert ad.iteracao_a_partir_etapa2 is None
        assert ad.tolerancia_processo_etapa2 is None
        assert ad.impressao_relatorio_etapa2 is None


def test_eq_curva():
    m: MagicMock = mock_open(read_data="".join(MockCurva))
    with patch("builtins.open", m):
        cf1 = Curva.read(ARQ_TESTE)
        cf2 = Curva.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_curva():
    m: MagicMock = mock_open(read_data="".join(MockCurva))
    with patch("builtins.open", m):
        cf1 = Curva.read(ARQ_TESTE)
        cf2 = Curva.read(ARQ_TESTE)
        cf2.curva_seguranca.iloc[0, 0] = -1
        assert cf1 != cf2


@pytest.mark.parametrize(
    "mock_arquivo",
    [MockCurva, MockCurvaComEspacos],
    ids=["sem_espacos", "com_espacos"],
)
def test_leitura_escrita_curva(mock_arquivo):
    m_leitura: MagicMock = mock_open(read_data="".join(mock_arquivo))
    with patch("builtins.open", m_leitura):
        cf1 = Curva.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = Curva.read(ARQ_TESTE)
        assert cf1 == cf2
