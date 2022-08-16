# Rotinas de testes associadas ao arquivo conft.dat do NEWAVE
from inewave.newave.modelos.conft import BlocoConfUTE

from inewave.newave import ConfT


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.conft import MockBlocoConfUTE


def test_bloco_ute_conft():

    m: MagicMock = mock_open(read_data="".join(MockBlocoConfUTE))
    b = BlocoConfUTE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 125
    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 209


def test_atributos_encontrados_conft():
    m: MagicMock = mock_open(read_data="".join(MockBlocoConfUTE))
    with patch("builtins.open", m):
        ad = ConfT.le_arquivo("")
        assert ad.usinas is not None


def test_atributos_nao_encontrados_conft():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = ConfT.le_arquivo("")
        assert ad.usinas is None


def test_eq_conft():
    m: MagicMock = mock_open(read_data="".join(MockBlocoConfUTE))
    with patch("builtins.open", m):
        cf1 = ConfT.le_arquivo("")
        cf2 = ConfT.le_arquivo("")
        assert cf1 == cf2


def test_neq_conft():
    m: MagicMock = mock_open(read_data="".join(MockBlocoConfUTE))
    with patch("builtins.open", m):
        cf1 = ConfT.le_arquivo("")
        cf2 = ConfT.le_arquivo("")
        cf2.usinas.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_conft():
    m_leitura: MagicMock = mock_open(read_data="".join(MockBlocoConfUTE))
    with patch("builtins.open", m_leitura):
        cf1 = ConfT.le_arquivo("")
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
        cf2 = ConfT.le_arquivo("")
        assert cf1 == cf2
