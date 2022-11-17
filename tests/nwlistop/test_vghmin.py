from inewave.nwlistop.vghmin import Vghmin

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vghmin import MockVghmin


def test_atributos_encontrados_vghmin():
    m: MagicMock = mock_open(read_data="".join(MockVghmin))
    with patch("builtins.open", m):
        n = Vghmin.le_arquivo("")
        assert n.ree is not None
        assert n.ree == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_vghmin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Vghmin.le_arquivo("")
        assert n.ree is None
        assert n.valores is None


def test_eq_vghmin():
    m: MagicMock = mock_open(read_data="".join(MockVghmin))
    with patch("builtins.open", m):
        n1 = Vghmin.le_arquivo("")
        n2 = Vghmin.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
