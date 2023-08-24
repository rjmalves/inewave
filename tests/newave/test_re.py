# Rotinas de testes associadas ao arquivo re.dat do NEWAVE
from inewave.newave.modelos.re import (
    BlocoUsinasConjuntoRE,
    BlocoConfiguracaoRestricoesRE,
)

from inewave.newave import Re


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.re import (
    MockBlocoUsinasRestricoes,
    MockBlocoRestricoes,
    MockRE,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_usinas_conjuntos_re():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUsinasRestricoes))
    b = BlocoUsinasConjuntoRE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 10
    assert b.data.iloc[-1, 1] == 284


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
        ad = Re.read(ARQ_TESTE)
        assert ad.usinas_conjuntos is not None
        assert ad.restricoes is not None


def test_atributos_nao_encontrados_re():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Re.read(ARQ_TESTE)
        assert ad.usinas_conjuntos is None
        assert ad.restricoes is None


def test_eq_re():
    m: MagicMock = mock_open(read_data="".join(MockRE))
    with patch("builtins.open", m):
        cf1 = Re.read(ARQ_TESTE)
        cf2 = Re.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_re():
    m: MagicMock = mock_open(read_data="".join(MockRE))
    with patch("builtins.open", m):
        cf1 = Re.read(ARQ_TESTE)
        cf2 = Re.read(ARQ_TESTE)
        cf2.usinas_conjuntos.loc[0, 0] = 0
        assert cf1 != cf2


def test_leitura_escrita_re():
    m_leitura: MagicMock = mock_open(read_data="".join(MockRE))
    with patch("builtins.open", m_leitura):
        cf1 = Re.read(ARQ_TESTE)
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
        cf2 = Re.read(ARQ_TESTE)
        assert cf1 == cf2
