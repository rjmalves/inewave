# Rotinas de testes associadas ao arquivo penalid.dat do NEWAVE

from inewave.newave.penalid import Penalid


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.penalid import (
    MockPenalid,
)


def test_atributos_encontrados_penalid():
    m: MagicMock = mock_open(read_data="".join(MockPenalid))
    with patch("builtins.open", m):
        ad = Penalid.le_arquivo("")
        assert ad.penalidades is not None


def test_atributos_nao_encontrados_penalid():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Penalid.le_arquivo("")
        assert ad.penalidades is None


def test_eq_penalid():
    m: MagicMock = mock_open(read_data="".join(MockPenalid))
    with patch("builtins.open", m):
        cf1 = Penalid.le_arquivo("")
        cf2 = Penalid.le_arquivo("")
        assert cf1 == cf2


def test_neq_penalid():
    m: MagicMock = mock_open(read_data="".join(MockPenalid))
    with patch("builtins.open", m):
        cf1 = Penalid.le_arquivo("")
        cf2 = Penalid.le_arquivo("")
        cf2.penalidades.loc[0, 0] = 0
        assert cf1 != cf2


def test_leitura_escrita_penalid():
    m_leitura: MagicMock = mock_open(read_data="".join(MockPenalid))
    with patch("builtins.open", m_leitura):
        cf1 = Penalid.le_arquivo("")
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
        cf2 = Penalid.le_arquivo("")
        assert cf1 == cf2
