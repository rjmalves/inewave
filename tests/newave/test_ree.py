# Rotinas de testes associadas ao arquivo ree.dat do NEWAVE
from inewave.newave.ree import REE


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ree import (
    MockREE,
)


def test_atributos_encontrados_ree():
    m: MagicMock = mock_open(read_data="".join(MockREE))
    with patch("builtins.open", m):
        ad = REE.le_arquivo("")
        assert ad.rees is not None
        assert ad.remocao_ficticias is not None


def test_atributos_nao_encontrados_ree():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = REE.le_arquivo("")
        assert ad.rees is None
        assert ad.remocao_ficticias is None


def test_eq_ree():
    m: MagicMock = mock_open(read_data="".join(MockREE))
    with patch("builtins.open", m):
        cf1 = REE.le_arquivo("")
        cf2 = REE.le_arquivo("")
        assert cf1 == cf2


def test_neq_ree():
    m: MagicMock = mock_open(read_data="".join(MockREE))
    with patch("builtins.open", m):
        cf1 = REE.le_arquivo("")
        cf2 = REE.le_arquivo("")
        cf2.rees.loc[0, 0] = 0
        assert cf1 != cf2


def test_leitura_escrita_ree():
    m_leitura: MagicMock = mock_open(read_data="".join(MockREE))
    with patch("builtins.open", m_leitura):
        cf1 = REE.le_arquivo("")
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
        cf2 = REE.le_arquivo("")
        assert cf1 == cf2
