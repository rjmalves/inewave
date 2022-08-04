from inewave.nwlistop.gttot import Gttot

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.gttot import MockGttot


def test_atributos_encontrados_gttot():
    m: MagicMock = mock_open(read_data="".join(MockGttot))
    with patch("builtins.open", m):
        n = Gttot.le_arquivo("")
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 2710.5


def test_atributos_nao_encontrados_gttot():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Gttot.le_arquivo("")
        assert n.submercado is None
        assert n.valores is None


def test_eq_gttot():
    m: MagicMock = mock_open(read_data="".join(MockGttot))
    with patch("builtins.open", m):
        n1 = Gttot.le_arquivo("")
        n2 = Gttot.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
