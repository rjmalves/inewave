from inewave.nwlistop.gttotsin import GttotSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.gttotsin import MockGttotsin


def test_atributos_encontrados_gttotsin():
    m: MagicMock = mock_open(read_data="".join(MockGttotsin))
    with patch("builtins.open", m):
        n = GttotSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 5106.0


def test_atributos_nao_encontrados_gttotsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = GttotSIN.le_arquivo("")
        assert n.valores is None


def test_eq_gttotsin():
    m: MagicMock = mock_open(read_data="".join(MockGttotsin))
    with patch("builtins.open", m):
        n1 = GttotSIN.le_arquivo("")
        n2 = GttotSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
