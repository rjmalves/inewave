# Rotinas de testes associadas ao arquivo confhd.dat do NEWAVE
from inewave.newave.modelos.confhd import BlocoConfUHE

from inewave.newave import Confhd


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.confhd import MockBlocoConfUHE


def test_bloco_uhe_confhd():

    m: MagicMock = mock_open(read_data="".join(MockBlocoConfUHE))
    b = BlocoConfUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 164
    assert b.data.iloc[0, 0] == 4
    assert b.data.iloc[-1, -1] == 1995


def test_atributos_encontrados_confhd():
    m: MagicMock = mock_open(read_data="".join(MockBlocoConfUHE))
    with patch("builtins.open", m):
        ad = Confhd.le_arquivo("")
        assert ad.usinas is not None


def test_atributos_nao_encontrados_confhd():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Confhd.le_arquivo("")
        assert ad.usinas is None


def test_eq_confhd():
    m: MagicMock = mock_open(read_data="".join(MockBlocoConfUHE))
    with patch("builtins.open", m):
        cf1 = Confhd.le_arquivo("")
        cf2 = Confhd.le_arquivo("")
        assert cf1 == cf2


def test_neq_confhd():
    m: MagicMock = mock_open(read_data="".join(MockBlocoConfUHE))
    with patch("builtins.open", m):
        cf1 = Confhd.le_arquivo("")
        cf2 = Confhd.le_arquivo("")
        cf2.usinas.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_confhd():
    m_leitura: MagicMock = mock_open(read_data="".join(MockBlocoConfUHE))
    with patch("builtins.open", m_leitura):
        cf1 = Confhd.le_arquivo("")
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
        cf2 = Confhd.le_arquivo("")
        assert cf1 == cf2
