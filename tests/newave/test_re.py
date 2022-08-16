# Rotinas de testes associadas ao arquivo re.dat do NEWAVE
from inewave.newave.modelos.re import (
    BlocoUsinasConjuntoRE,
    BlocoConfiguracaoRestricoesRE,
)

from inewave.newave import RE


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.re import (
    MockBlocoUsinasRestricoes,
    MockBlocoRestricoes,
    MockRE,
)


def test_bloco_usinas_conjuntos_re():

    m: MagicMock = mock_open(read_data="".join(MockBlocoUsinasRestricoes))
    b = BlocoUsinasConjuntoRE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 10
    assert b.data.iloc[-1, 2] == 284


def test_bloco_restricoes_re():

    m: MagicMock = mock_open(read_data="".join(MockBlocoRestricoes))
    b = BlocoConfiguracaoRestricoesRE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 10
    assert b.data.iloc[-1, -1] == "C. CALDEIRAO E F. GOMES"


def test_atributos_encontrados_re():
    m: MagicMock = mock_open(read_data="".join(MockRE))
    with patch("builtins.open", m):
        ad = RE.le_arquivo("")
        assert ad.usinas_conjuntos is not None
        assert ad.restricoes is not None


def test_atributos_nao_encontrados_re():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = RE.le_arquivo("")
        assert ad.usinas_conjuntos is None
        assert ad.restricoes is None


def test_eq_re():
    m: MagicMock = mock_open(read_data="".join(MockRE))
    with patch("builtins.open", m):
        cf1 = RE.le_arquivo("")
        cf2 = RE.le_arquivo("")
        assert cf1 == cf2


def test_neq_re():
    m: MagicMock = mock_open(read_data="".join(MockRE))
    with patch("builtins.open", m):
        cf1 = RE.le_arquivo("")
        cf2 = RE.le_arquivo("")
        cf2.usinas_conjuntos.loc[0, 0] = 0
        assert cf1 != cf2


def test_leitura_escrita_re():
    m_leitura: MagicMock = mock_open(read_data="".join(MockRE))
    with patch("builtins.open", m_leitura):
        cf1 = RE.le_arquivo("")
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
        cf2 = RE.le_arquivo("")
        assert cf1 == cf2
