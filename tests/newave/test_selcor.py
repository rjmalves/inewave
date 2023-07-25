# Rotinas de testes associadas ao arquivo selcor.dat do NEWAVE
from inewave.newave.modelos.selcor import BlocoDadosSelcor

from inewave.newave import Selcor


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.selcor import MockSelcor

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_usinas_selcor():
    m: MagicMock = mock_open(read_data="".join(MockSelcor))
    b = BlocoDadosSelcor()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)
    assert len(b.data) == 7
    assert b.data[0][0] == 2
    assert b.data[1][0] == 0
    assert b.data[2][0] == 12
    assert b.data[3][0] == 1
    assert b.data[4][0] == 0
    assert b.data[5] == [7, 15]
    assert b.data[6] == [2, 9]


def test_atributos_encontrados_selcor():
    m: MagicMock = mock_open(read_data="".join(MockSelcor))
    with patch("builtins.open", m):
        ad = Selcor.read(ARQ_TESTE)
        assert ad.iteracao_inicial is not None
        assert ad.tamanho_janela is not None
        assert ad.numero_cortes_adicionados_por_iteracao is not None
        assert ad.considera_cortes_da_propria_iteracao is not None
        assert ad.imprime_relatorio is not None
        assert ad.iteracoes_impressao is not None
        assert ad.series_impressao is not None


def test_atributos_nao_encontrados_selcor():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Selcor.read(ARQ_TESTE)
        assert ad.iteracao_inicial is None
        assert ad.tamanho_janela is None
        assert ad.numero_cortes_adicionados_por_iteracao is None
        assert ad.considera_cortes_da_propria_iteracao is None
        assert ad.imprime_relatorio is None
        assert ad.iteracoes_impressao == [None, None]
        assert ad.series_impressao == [None, None]


def test_eq_selcor():
    m: MagicMock = mock_open(read_data="".join(MockSelcor))
    with patch("builtins.open", m):
        cf1 = Selcor.read(ARQ_TESTE)
        cf2 = Selcor.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_selcor():
    m: MagicMock = mock_open(read_data="".join(MockSelcor))
    with patch("builtins.open", m):
        cf1 = Selcor.read(ARQ_TESTE)
        cf2 = Selcor.read(ARQ_TESTE)
        cf2.iteracao_inicial = 1
        assert cf1 != cf2


def test_leitura_escrita_selcor():
    m_leitura: MagicMock = mock_open(read_data="".join(MockSelcor))
    with patch("builtins.open", m_leitura):
        cf1 = Selcor.read(ARQ_TESTE)
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
        cf2 = Selcor.read(ARQ_TESTE)
        assert cf1 == cf2
