# Rotinas de testes associadas ao arquivo volref_saz.dat do NEWAVE
from inewave.newave.modelos.volref_saz import BlocoVolrefSaz

from inewave.newave import VolrefSaz


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.volref_saz import MockVolrefSaz

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_desvios_volrefsaz():
    m: MagicMock = mock_open(read_data="".join(MockVolrefSaz))
    b = BlocoVolrefSaz()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 2040
    assert b.data.iloc[0, 0] == 4
    assert b.data.iloc[-1, -1] == 0.0


def test_atributos_encontrados_volrefsaz():
    m: MagicMock = mock_open(read_data="".join(MockVolrefSaz))
    with patch("builtins.open", m):
        ad = VolrefSaz.read(ARQ_TESTE)
        assert ad.volumes is not None


def test_atributos_nao_encontrados_volrefsaz():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = VolrefSaz.read(ARQ_TESTE)
        assert ad.volumes is None


def test_eq_volrefsaz():
    m: MagicMock = mock_open(read_data="".join(MockVolrefSaz))
    with patch("builtins.open", m):
        cf1 = VolrefSaz.read(ARQ_TESTE)
        cf2 = VolrefSaz.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_volrefsaz():
    m: MagicMock = mock_open(read_data="".join(MockVolrefSaz))
    with patch("builtins.open", m):
        cf1 = VolrefSaz.read(ARQ_TESTE)
        cf2 = VolrefSaz.read(ARQ_TESTE)
        cf2.volumes.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_volrefsaz():
    m_leitura: MagicMock = mock_open(read_data="".join(MockVolrefSaz))
    with patch("builtins.open", m_leitura):
        cf1 = VolrefSaz.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = VolrefSaz.read(ARQ_TESTE)
        assert cf1 == cf2
