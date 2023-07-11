# Rotinas de testes associadas ao arquivo shist.dat do NEWAVE
from inewave.newave.modelos.shist import (
    BlocoVarreduraShist,
    BlocoSeriesSimulacaoShist,
)

from inewave.newave import Shist


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.shist import (
    MockBlocoVarreduraShist,
    MockBlocoSeriesSimulacaoShist,
    MockShist,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_varredura_shist():
    m: MagicMock = mock_open(read_data="".join(MockBlocoVarreduraShist))
    b = BlocoVarreduraShist()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == [1, 1932]


def test_bloco_series_shist():
    m: MagicMock = mock_open(read_data="".join(MockBlocoSeriesSimulacaoShist))
    b = BlocoSeriesSimulacaoShist()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == []


def test_atributos_encontrados_shist():
    m: MagicMock = mock_open(read_data="".join(MockShist))
    with patch("builtins.open", m):
        ad = Shist.read(ARQ_TESTE)
        assert ad.varredura is not None
        assert ad.ano_inicio_varredura is not None
        assert ad.anos_inicio_simulacoes is not None


def test_atributos_nao_encontrados_shist():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Shist.read(ARQ_TESTE)
        assert ad.varredura is None
        assert ad.ano_inicio_varredura is None
        assert ad.anos_inicio_simulacoes == []


def test_eq_shist():
    m: MagicMock = mock_open(read_data="".join(MockShist))
    with patch("builtins.open", m):
        cf1 = Shist.read(ARQ_TESTE)
        cf2 = Shist.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_shist():
    m: MagicMock = mock_open(read_data="".join(MockShist))
    with patch("builtins.open", m):
        cf1 = Shist.read(ARQ_TESTE)
        cf2 = Shist.read(ARQ_TESTE)
        cf2.varredura = 0
        assert cf1 != cf2


def test_leitura_escrita_shist():
    m_leitura: MagicMock = mock_open(read_data="".join(MockShist))
    with patch("builtins.open", m_leitura):
        cf1 = Shist.read(ARQ_TESTE)
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
        cf2 = Shist.read(ARQ_TESTE)
        assert cf1 == cf2
