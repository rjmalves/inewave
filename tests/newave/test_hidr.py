from inewave.newave.modelos.hidr import RegistroUHEHidr
from inewave.newave.hidr import Hidr

from os.path import join
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TEST = "./tests/mocks/arquivos"


def test_registro_uhe_hidr():

    r = RegistroUHEHidr()
    with open(join(ARQ_TEST, "hidr.dat"), "rb") as fp:
        r.read(fp, storage="BINARY")

    assert len(r.data) == 111
    assert r.nome == "CAMARGOS"


def test_atributos_encontrados_hidr():
    h = Hidr.le_arquivo(ARQ_TEST)
    assert h.cadastro is not None


def test_atributos_nao_encontrados_hidr():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Hidr.le_arquivo("")
        assert ad.cadastro is None


def test_eq_hidr():
    h1 = Hidr.le_arquivo(ARQ_TEST)
    h2 = Hidr.le_arquivo(ARQ_TEST)
    assert h1 == h2


def test_neq_hidr():
    h1 = Hidr.le_arquivo(ARQ_TEST)
    h2 = Hidr.le_arquivo(ARQ_TEST)
    h2.cadastro.iloc[0, 0] = "TESTE"
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h2.escreve_arquivo("")
        assert h1 != h2


def test_leitura_escrita_hidr():
    h1 = Hidr.le_arquivo(ARQ_TEST)
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
        h2 = Hidr.le_arquivo("")
        assert h1 == h2
