# Rotinas de testes associadas ao arquivo agrint.dat do NEWAVE
from inewave.newave.modelos.agrint import (
    BlocoGruposAgrint,
    BlocoLimitesPorGrupoAgrint,
)

from inewave.newave import Agrint


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.agrint import (
    MockBlocoGruposAgrint,
    MockBlocoLimitesPorGrupoAgrint,
    MockAgrint,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_grupos_agrint():
    m: MagicMock = mock_open(read_data="".join(MockBlocoGruposAgrint))
    b = BlocoGruposAgrint()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 14
    assert b.data.iloc[-1, 2] == 1


def test_bloco_limites_agrint():
    m: MagicMock = mock_open(read_data="".join(MockBlocoLimitesPorGrupoAgrint))
    b = BlocoLimitesPorGrupoAgrint()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 14
    assert b.data.iloc[-1, -1] == 17923


def test_atributos_encontrados_agrint():
    m: MagicMock = mock_open(read_data="".join(MockAgrint))
    with patch("builtins.open", m):
        ad = Agrint.read(ARQ_TESTE)
        assert ad.agrupamentos is not None
        assert ad.limites_agrupamentos is not None


def test_atributos_nao_encontrados_agrint():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Agrint.read(ARQ_TESTE)
        assert ad.agrupamentos is None
        assert ad.limites_agrupamentos is None


def test_eq_agrint():
    m: MagicMock = mock_open(read_data="".join(MockAgrint))
    with patch("builtins.open", m):
        cf1 = Agrint.read(ARQ_TESTE)
        cf2 = Agrint.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_agrint():
    m: MagicMock = mock_open(read_data="".join(MockAgrint))
    with patch("builtins.open", m):
        cf1 = Agrint.read(ARQ_TESTE)
        cf2 = Agrint.read(ARQ_TESTE)
        cf2.agrupamentos.loc[0, 0] = 0
        assert cf1 != cf2


def test_leitura_escrita_agrint():
    m_leitura: MagicMock = mock_open(read_data="".join(MockAgrint))
    with patch("builtins.open", m_leitura):
        cf1 = Agrint.read(ARQ_TESTE)
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
        cf2 = Agrint.read(ARQ_TESTE)
        assert cf1 == cf2
