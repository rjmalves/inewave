from inewave.newave.modelos.vazoes import RegistroVazoesPostos
from inewave.newave.vazoes import Vazoes

from os.path import join
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TEST = "./tests/mocks/arquivos"


def test_registro_vazoesposto_vazoes():

    r = RegistroVazoesPostos()
    with open(join(ARQ_TEST, "vazoes.dat"), "rb") as fp:
        r.read(fp, storage="BINARY")

    assert len(r.data) == 320


def test_atributos_encontrados_vazoes():
    h = Vazoes.le_arquivo(ARQ_TEST)
    assert h.vazoes is not None


def test_atributos_nao_encontrados_vazoes():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Vazoes.le_arquivo("")
        assert ad.vazoes is None


def test_eq_vazoes():
    h1 = Vazoes.le_arquivo(ARQ_TEST)
    h2 = Vazoes.le_arquivo(ARQ_TEST)
    assert h1 == h2


def test_neq_vazoes():
    h1 = Vazoes.le_arquivo(ARQ_TEST)
    h2 = Vazoes.le_arquivo(ARQ_TEST)
    h2.vazoes.iloc[0, 0] = -1
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h2.escreve_arquivo("")
        assert h1 != h2


def test_leitura_escrita_vazoes():
    h1 = Vazoes.le_arquivo(ARQ_TEST)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        h1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data=b"".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        h2 = Vazoes.le_arquivo("")
        assert h1 == h2


def test_leitura_escrita_editando_vazoes():
    h1 = Vazoes.le_arquivo(ARQ_TEST)
    vaz = h1.vazoes
    num_vazoes_original = vaz.shape[0]
    h1.vazoes.loc[vaz.shape[0]] = 0
    m_escrita: MagicMock = mock_open(read_data="")
    # Testa aumentando a quantidade de vazões
    with patch("builtins.open", m_escrita):
        h1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
        assert len(linhas_escritas) == num_vazoes_original
    # Testa reduzindo a quantidade de vazões
    num_vazoes_reduzidas = 10
    h1.vazoes.drop(
        index=list(range(num_vazoes_reduzidas, num_vazoes_original + 1)),
        inplace=True,
    )
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        h1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
        assert len(linhas_escritas) == num_vazoes_reduzidas
