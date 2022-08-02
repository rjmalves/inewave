from inewave.nwlistop.gttot00 import Gttot00

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.gttot00 import MockGttot00


def test_atributos_encontrados_gttot00():
    m: MagicMock = mock_open(read_data="".join(MockGttot00))
    with patch("builtins.open", m):
        n = Gttot00.le_arquivo("")
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 2710.5


def test_atributos_nao_encontrados_gttot00():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Gttot00.le_arquivo("")
        assert n.submercado is None
        assert n.valores is None


def test_eq_gttot00():
    m: MagicMock = mock_open(read_data="".join(MockGttot00))
    with patch("builtins.open", m):
        n1 = Gttot00.le_arquivo("")
        n2 = Gttot00.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
