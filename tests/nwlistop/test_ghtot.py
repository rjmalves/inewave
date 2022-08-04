from inewave.nwlistop.ghtot import Ghtot

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghtot import MockGhtot


def test_atributos_encontrados_ghtot():
    m: MagicMock = mock_open(read_data="".join(MockGhtot))
    with patch("builtins.open", m):
        n = Ghtot.le_arquivo("")
        assert n.ree is not None
        assert n.ree == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 2578.7


def test_atributos_nao_encontrados_ghtot():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Ghtot.le_arquivo("")
        assert n.ree is None
        assert n.valores is None


def test_eq_ghtot():
    m: MagicMock = mock_open(read_data="".join(MockGhtot))
    with patch("builtins.open", m):
        n1 = Ghtot.le_arquivo("")
        n2 = Ghtot.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
