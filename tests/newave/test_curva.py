# Rotinas de testes associadas ao arquivo curva.dat do NEWAVE
from inewave.newave.modelos.curva import (
    BlocoConfiguracoesPenalizacaoCurva,
    BlocoPenalidadesViolacaoREECurva,
    BlocoCurvaSegurancaSubsistema,
    BlocoMaximoIteracoesProcessoIterativoEtapa2,
    BlocoIteracaoAPartirProcessoIterativoEtapa2,
    BlocoToleranciaProcessoIterativoEtapa2,
    BlocoImpressaoRelatorioProcessoIterativoEtapa2,
)

from inewave.newave import Curva


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
)


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
    b = BlocoCurvaSegurancaSubsistema()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 10.0


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
        ad = Curva.le_arquivo("")
        assert ad.configuracoes_penalizacao != [None, None, None]
        assert ad.custos_penalidades is not None
        assert ad.curva_seguranca is not None
        assert ad.maximo_iteracoes_etapa2 is not None
        assert ad.iteracao_a_partir_etapa2 is not None
        assert ad.tolerancia_processo_etapa2 is not None
        assert ad.impressao_relatorio_etapa2 is not None


def test_atributos_nao_encontrados_curva():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Curva.le_arquivo("")
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
        cf1 = Curva.le_arquivo("")
        cf2 = Curva.le_arquivo("")
        assert cf1 == cf2


def test_neq_curva():
    m: MagicMock = mock_open(read_data="".join(MockCurva))
    with patch("builtins.open", m):
        cf1 = Curva.le_arquivo("")
        cf2 = Curva.le_arquivo("")
        cf2.curva_seguranca.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_curva():
    m_leitura: MagicMock = mock_open(read_data="".join(MockCurva))
    with patch("builtins.open", m_leitura):
        cf1 = Curva.le_arquivo("")
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(2, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = Curva.le_arquivo("")
        assert cf1 == cf2
