# Rotinas de testes associadas ao arquivo term.dat do NEWAVE
from inewave.config import MESES_DF
from inewave.newave.modelos.term import BlocoTermUTE

from inewave.newave import Term


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.term import MockBlocoUTE


def test_bloco_usinas_term():

    m: MagicMock = mock_open(read_data="".join(MockBlocoUTE))
    b = BlocoTermUTE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)
    assert b.data.shape[0] == 125
    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 63.0


def test_atributos_encontrados_term():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTE))
    with patch("builtins.open", m):
        ad = Term.le_arquivo("")
        assert ad.usinas is not None


def test_atributos_nao_encontrados_term():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Term.le_arquivo("")
        assert ad.usinas is None


def test_eq_term():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTE))
    with patch("builtins.open", m):
        cf1 = Term.le_arquivo("")
        cf2 = Term.le_arquivo("")
        assert cf1 == cf2


def test_neq_term():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTE))
    with patch("builtins.open", m):
        cf1 = Term.le_arquivo("")
        cf2 = Term.le_arquivo("")
        cf2.usinas.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_term():
    m_leitura: MagicMock = mock_open(read_data="".join(MockBlocoUTE))
    with patch("builtins.open", m_leitura):
        cf1 = Term.le_arquivo("")
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
        cf2 = Term.le_arquivo("")
        assert cf1 == cf2
