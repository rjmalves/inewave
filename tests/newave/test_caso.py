from inewave.newave.modelos.caso import NomeCaso, CaminhoGerenciadorProcessos
from inewave.newave import Caso

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.caso import (
    MockNomeCaso,
    MockCaminhoGerenciador,
    MockCaso,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


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
        ad = Caso.read(ARQ_TESTE)
        assert ad.arquivos is not None
        assert ad.gerenciador_processos is not None


def test_atributos_nao_encontrados_caso():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Caso.read(ARQ_TESTE)
        assert ad.arquivos == ""
        assert ad.gerenciador_processos == ""


def test_eq_caso():
    m: MagicMock = mock_open(read_data="".join(MockCaso))
    with patch("builtins.open", m):
        ad1 = Caso.read(ARQ_TESTE)
        ad2 = Caso.read(ARQ_TESTE)
        assert ad1 == ad2


def test_neq_caso():
    m: MagicMock = mock_open(read_data="".join(MockCaso))
    with patch("builtins.open", m):
        ad1 = Caso.read(ARQ_TESTE)
        ad2 = Caso.read(ARQ_TESTE)
        ad2.gerenciador_processos = "/bin"
        assert ad1 != ad2


def test_leitura_escrita_caso():
    m_leitura: MagicMock = mock_open(read_data="".join(MockCaso))
    with patch("builtins.open", m_leitura):
        ad1 = Caso.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ad1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ad2 = Caso.read(ARQ_TESTE)
        assert ad1 == ad2
