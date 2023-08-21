# Rotinas de testes associadas ao arquivo dsvagua.dat do NEWAVE
from inewave.newave.modelos.dsvagua import BlocoDsvUHE

from inewave.newave import Dsvagua


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.dsvagua import MockBlocoDesviosAgua

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_desvios_dsvagua():
    m: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    b = BlocoDsvUHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12540
    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 306


def test_atributos_encontrados_dsvagua():
    m: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    with patch("builtins.open", m):
        ad = Dsvagua.read(ARQ_TESTE)
        assert ad.desvios is not None


def test_atributos_nao_encontrados_dsvagua():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Dsvagua.read(ARQ_TESTE)
        assert ad.desvios is None


def test_eq_dsvagua():
    m: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    with patch("builtins.open", m):
        cf1 = Dsvagua.read(ARQ_TESTE)
        cf2 = Dsvagua.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_dsvagua():
    m: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    with patch("builtins.open", m):
        cf1 = Dsvagua.read(ARQ_TESTE)
        cf2 = Dsvagua.read(ARQ_TESTE)
        cf2.desvios.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_dsvagua():
    m_leitura: MagicMock = mock_open(read_data="".join(MockBlocoDesviosAgua))
    with patch("builtins.open", m_leitura):
        cf1 = Dsvagua.read(ARQ_TESTE)
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
        cf2 = Dsvagua.read(ARQ_TESTE)
        cf1.desvios.sort_values(
            ["codigo_usina", "comentario", "data"], inplace=True
        )
        cf2.desvios.sort_values(
            ["codigo_usina", "comentario", "data"], inplace=True
        )
        cf1.desvios.reset_index(drop=True, inplace=True)
        cf2.desvios.reset_index(drop=True, inplace=True)
        assert cf1 == cf2
