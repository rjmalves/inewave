from inewave.newave.modelos.caso import NomeCaso, CaminhoGerenciadorProcessos
from inewave.newave import Caso

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.caso import (
    MockNomeCaso,
    MockCaminhoGerenciador,
    MockCaso,
)


def test_bloco_nome_caso():

    m: MagicMock = mock_open(read_data="".join(MockNomeCaso))
    b = NomeCaso()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == "arquivos.dat"


def test_bloco_caminho_gerenciador_caso():

    m: MagicMock = mock_open(read_data="".join(MockCaminhoGerenciador))
    b = CaminhoGerenciadorProcessos()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == "/home/newave/"


def test_atributos_encontrados_caso():
    m: MagicMock = mock_open(read_data="".join(MockCaso))
    with patch("builtins.open", m):
        ad = Caso.le_arquivo("")
        assert ad.arquivos is not None
        assert ad.gerenciador_processos is not None


def test_atributos_nao_encontrados_caso():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Caso.le_arquivo("")
        assert ad.arquivos == ""
        assert ad.gerenciador_processos == ""


def test_eq_caso():
    m: MagicMock = mock_open(read_data="".join(MockCaso))
    with patch("builtins.open", m):
        ad1 = Caso.le_arquivo("")
        ad2 = Caso.le_arquivo("")
        assert ad1 == ad2


def test_neq_caso():
    m: MagicMock = mock_open(read_data="".join(MockCaso))
    with patch("builtins.open", m):
        ad1 = Caso.le_arquivo("")
        ad2 = Caso.le_arquivo("")
        ad2.gerenciador_processos = "/bin"
        assert ad1 != ad2


def test_leitura_escrita_caso():
    m_leitura: MagicMock = mock_open(read_data="".join(MockCaso))
    with patch("builtins.open", m_leitura):
        ad1 = Caso.le_arquivo("")
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
        ad2 = Caso.le_arquivo("")
        assert ad1 == ad2
