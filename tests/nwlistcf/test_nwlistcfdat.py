from inewave.nwlistcf.modelos.nwlistcfdat import (
    PeriodoImpressaoCortesEstados,
    OpcoesImpressao,
)
from inewave.nwlistcf import Nwlistcfdat

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.nwlistcfdat import (
    MockBlocoPeriodoImpressao,
    MockBlocoOpcoesImpressao,
    MockNwlistcfdat,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_periodo_impressao_nwlistcfdat():
    m: MagicMock = mock_open(read_data="".join(MockBlocoPeriodoImpressao))
    b = PeriodoImpressaoCortesEstados()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)
    assert b.data == [3, 60, 0]


def test_bloco_opcoes_impressao_nwlistcfdat():
    m: MagicMock = mock_open(read_data="".join(MockBlocoOpcoesImpressao))
    b = OpcoesImpressao()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)
    assert b.data == [99, None, None]


def test_atributos_encontrados_nwlistcfdat():
    m: MagicMock = mock_open(read_data="".join(MockNwlistcfdat))
    with patch("builtins.open", m):
        n = Nwlistcfdat.read(ARQ_TESTE)
        assert n.mes_inicio is not None
        assert n.mes_fim is not None
        assert n.imprime_cortes_ativos is not None
        assert n.opcoes_impressao is not None


def test_atributos_nao_encontrados_nwlistcfdat():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Nwlistcfdat.read(ARQ_TESTE)
        assert n.mes_inicio is None
        assert n.mes_fim is None
        assert n.imprime_cortes_ativos is None
        assert n.opcoes_impressao == [None, None, None]


def test_eq_nwlistcfdat():
    m: MagicMock = mock_open(read_data="".join(MockNwlistcfdat))
    with patch("builtins.open", m):
        n1 = Nwlistcfdat.read(ARQ_TESTE)
        n2 = Nwlistcfdat.read(ARQ_TESTE)
        assert n1 == n2


def test_eq_nwlistcfdat():
    m: MagicMock = mock_open(read_data="".join(MockNwlistcfdat))
    with patch("builtins.open", m):
        n1 = Nwlistcfdat.read(ARQ_TESTE)
        n1.mes_inicio = 11
        n2 = Nwlistcfdat.read(ARQ_TESTE)
        assert n1 != n2


def test_leitura_escrita_nwlistcfdat():
    m_leitura: MagicMock = mock_open(read_data="".join(MockNwlistcfdat))
    with patch("builtins.open", m_leitura):
        nc1 = Nwlistcfdat.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        nc1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        nc2 = Nwlistcfdat.read(ARQ_TESTE)
        assert nc1 == nc2
