# Rotinas de testes associadas ao arquivo eafpast.dat do NEWAVE
from inewave.newave.modelos.eafpast import BlocoEafPast

from inewave.newave import EafPast


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eafpast import MockBlocoAfluenciasPassadas


def test_bloco_desvios_eafpast():

    m: MagicMock = mock_open(read_data="".join(MockBlocoAfluenciasPassadas))
    b = BlocoEafPast()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)
    assert b.data.shape[0] == 12
    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 544.91


def test_atributos_encontrados_eafpast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoAfluenciasPassadas))
    with patch("builtins.open", m):
        ad = EafPast.le_arquivo("")
        assert ad.tendencia is not None


def test_atributos_nao_encontrados_eafpast():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = EafPast.le_arquivo("")
        assert ad.tendencia is None


def test_eq_eafpast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoAfluenciasPassadas))
    with patch("builtins.open", m):
        cf1 = EafPast.le_arquivo("")
        cf2 = EafPast.le_arquivo("")
        assert cf1 == cf2


def test_neq_eafpast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoAfluenciasPassadas))
    with patch("builtins.open", m):
        cf1 = EafPast.le_arquivo("")
        cf2 = EafPast.le_arquivo("")
        cf2.tendencia.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_eafpast():
    m_leitura: MagicMock = mock_open(
        read_data="".join(MockBlocoAfluenciasPassadas)
    )
    with patch("builtins.open", m_leitura):
        cf1 = EafPast.le_arquivo("")
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
        cf2 = EafPast.le_arquivo("")
        assert cf1 == cf2
