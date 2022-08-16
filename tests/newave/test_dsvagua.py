# Rotinas de testes associadas ao arquivo dsvagua.dat do NEWAVE
from inewave.newave.modelos.dsvagua import BlocoDsvUHE

from inewave.newave import DSVAgua


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.dsvagua import MockBlocoDesviosAgua


def test_bloco_desvios_dsvagua():

    m: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    b = BlocoDsvUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 1045
    assert b.data.iloc[0, 0] == 2020
    assert b.data.iloc[-1, 0] == 2024


def test_atributos_encontrados_dsvagua():
    m: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    with patch("builtins.open", m):
        ad = DSVAgua.le_arquivo("")
        assert ad.desvios is not None


def test_atributos_nao_encontrados_dsvagua():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = DSVAgua.le_arquivo("")
        assert ad.desvios is None


def test_eq_dsvagua():
    m: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    with patch("builtins.open", m):
        cf1 = DSVAgua.le_arquivo("")
        cf2 = DSVAgua.le_arquivo("")
        assert cf1 == cf2


def test_neq_dsvagua():
    m: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    with patch("builtins.open", m):
        cf1 = DSVAgua.le_arquivo("")
        cf2 = DSVAgua.le_arquivo("")
        cf2.desvios.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_dsvagua():
    m_leitura: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    with patch("builtins.open", m_leitura):
        cf1 = DSVAgua.le_arquivo("")
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
        cf2 = DSVAgua.le_arquivo("")
        assert cf1 == cf2
