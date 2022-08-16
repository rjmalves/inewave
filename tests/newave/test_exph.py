from datetime import datetime
from inewave.newave.modelos.exph import BlocoUHEExph
from inewave.newave import Exph

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.exph import MockExph


def test_bloco_uhe_exph():

    m: MagicMock = mock_open(read_data="".join(MockExph))
    b = BlocoUHEExph()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 7
    assert b.data.shape[1] == 9
    assert b.data.iloc[0, 0] == 309
    assert b.data.iloc[0, 1] == "JURUENA"
    assert b.data.iloc[0, 2] == datetime(2024, 10, 1)
    assert b.data.iloc[0, 3] == 3
    assert b.data.iloc[0, 4] == 0.0
    assert b.data.iloc[1, 5] == datetime(2025, 1, 1)
    assert b.data.iloc[1, 6] == 25.0
    assert b.data.iloc[1, 7] == 1
    assert b.data.iloc[1, 8] == 1
    assert b.data.iloc[-1, -1] == 3


def test_atributos_encontrados_exph():
    m: MagicMock = mock_open(read_data="".join(MockExph))
    with patch("builtins.open", m):
        ad = Exph.le_arquivo("")
        assert ad.expansoes is not None


def test_atributos_nao_encontrados_exph():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Exph.le_arquivo("")
        assert ad.expansoes is None


def test_eq_exph():
    m: MagicMock = mock_open(read_data="".join(MockExph))
    with patch("builtins.open", m):
        ad1 = Exph.le_arquivo("")
        ad2 = Exph.le_arquivo("")
        assert ad1 == ad2


def test_neq_exph():
    m: MagicMock = mock_open(read_data="".join(MockExph))
    with patch("builtins.open", m):
        ad1 = Exph.le_arquivo("")
        ad2 = Exph.le_arquivo("")
        ad2.expansoes.iloc[0, 0] = -1
        assert ad1 != ad2


def test_leitura_escrita_exph():
    m_leitura: MagicMock = mock_open(read_data="".join(MockExph))
    with patch("builtins.open", m_leitura):
        ad1 = Exph.le_arquivo("")
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
        ad2 = Exph.le_arquivo("")
        assert ad1 == ad2
