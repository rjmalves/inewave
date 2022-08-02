from inewave.nwlistop.vertuh import VertUH

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vertuh import MockVertuh


def test_atributos_encontrados_vertuh():
    m: MagicMock = mock_open(read_data="".join(MockVertuh))
    with patch("builtins.open", m):
        n = VertUH.le_arquivo("")
        assert n.usina is not None
        assert n.usina == "ESPORA"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 30.74


def test_atributos_nao_encontrados_vertuh():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = VertUH.le_arquivo("")
        assert n.usina is None
        assert n.valores is None


def test_eq_vertuh():
    m: MagicMock = mock_open(read_data="".join(MockVertuh))
    with patch("builtins.open", m):
        n1 = VertUH.le_arquivo("")
        n2 = VertUH.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
