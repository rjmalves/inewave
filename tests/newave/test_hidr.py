from inewave.newave.modelos.hidr import RegistroUHEHidr
from inewave.newave.hidr import Hidr


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TESTE = "./tests/mocks/arquivos/hidr.dat"


def test_registro_uhe_hidr():
    r = RegistroUHEHidr()
    with open(ARQ_TESTE, "rb") as fp:
        r.read(fp, storage="BINARY")

    assert len(r.data) == 111
    assert r.nome == "CAMARGOS"


def test_atributos_encontrados_hidr():
    h = Hidr.read(ARQ_TESTE)
    assert h.cadastro is not None


def test_atributos_nao_encontrados_hidr():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Hidr.read(ARQ_TESTE)
        assert ad.cadastro is None


def test_eq_hidr():
    h1 = Hidr.read(ARQ_TESTE)
    h2 = Hidr.read(ARQ_TESTE)
    assert h1 == h2


def test_neq_hidr():
    h1 = Hidr.read(ARQ_TESTE)
    h2 = Hidr.read(ARQ_TESTE)
    h2.cadastro.iloc[0, 0] = "TESTE"
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h2.write(ARQ_TESTE)
        assert h1 != h2


def test_leitura_escrita_hidr():
    h1 = Hidr.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        h1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data=b"".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        h2 = Hidr.read(ARQ_TESTE)
        assert h1 == h2
