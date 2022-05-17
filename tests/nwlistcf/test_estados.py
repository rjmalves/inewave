from inewave.nwlistcf import Estados

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.estados import MockEstados


def test_atributos_encontrados_estados():
    m: MagicMock = mock_open(read_data="".join(MockEstados))
    with patch("builtins.open", m):
        n = Estados.le_arquivo("")
        assert n.estados is not None


def test_atributos_nao_encontrados_estados():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Estados.le_arquivo("")
        assert n.estados is None


def test_eq_estados():
    m: MagicMock = mock_open(read_data="".join(MockEstados))
    with patch("builtins.open", m):
        n1 = Estados.le_arquivo("")
        n2 = Estados.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
