from inewave.nwlistop.cmarg import Cmarg

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cmarg import MockCmarg


def test_atributos_encontrados_cmarg():
    m: MagicMock = mock_open(read_data="".join(MockCmarg))
    with patch("builtins.open", m):
        n = Cmarg.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 1995
        assert n.valores.iloc[-1, -1] == 35.42
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_cmarg():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Cmarg.le_arquivo("")
        assert n.valores is None
        assert n.submercado is None


def test_eq_cmarg():
    m: MagicMock = mock_open(read_data="".join(MockCmarg))
    with patch("builtins.open", m):
        n1 = Cmarg.le_arquivo("")
        n2 = Cmarg.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
