from inewave.nwlistcf import Estados

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.estados import MockEstados

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_estados():
    m: MagicMock = mock_open(read_data="".join(MockEstados))
    with patch("builtins.open", m):
        n = Estados.read(ARQ_TESTE)
        assert n.estados is not None


def test_atributos_nao_encontrados_estados():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Estados.read(ARQ_TESTE)
        assert n.estados is None


def test_eq_estados():
    m: MagicMock = mock_open(read_data="".join(MockEstados))
    with patch("builtins.open", m):
        n1 = Estados.read(ARQ_TESTE)
        n2 = Estados.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
