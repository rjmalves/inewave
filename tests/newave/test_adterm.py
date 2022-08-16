from inewave.newave.modelos.adterm import BlocoUTEAdTerm
from inewave.newave import AdTerm

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.adterm import MockBlocoUTEAdTerm


def test_bloco_ute_adterm():

    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEAdTerm))
    b = BlocoUTEAdTerm()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 6
    assert b.data.shape[1] == 6
    assert b.data.iloc[0, 3] == 230.70
    assert b.data.iloc[-1, -1] == 0.00


def test_atributos_encontrados_adterm():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEAdTerm))
    with patch("builtins.open", m):
        ad = AdTerm.le_arquivo("")
        assert ad.despachos is not None


def test_atributos_nao_encontrados_adterm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = AdTerm.le_arquivo("")
        assert ad.despachos is None


def test_eq_adterm():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEAdTerm))
    with patch("builtins.open", m):
        ad1 = AdTerm.le_arquivo("")
        ad2 = AdTerm.le_arquivo("")
        assert ad1 == ad2


def test_neq_adterm():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEAdTerm))
    with patch("builtins.open", m):
        ad1 = AdTerm.le_arquivo("")
        ad2 = AdTerm.le_arquivo("")
        ad2.despachos.iloc[0, 0] = -1
        assert ad1 != ad2


def test_leitura_escrita_adterm():
    m_leitura: MagicMock = mock_open(read_data="".join(MockBlocoUTEAdTerm))
    with patch("builtins.open", m_leitura):
        ad1 = AdTerm.le_arquivo("")
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ad1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(2, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ad2 = AdTerm.le_arquivo("")
        assert ad1 == ad2
