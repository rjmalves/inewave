from inewave.nwlistop.eafb import Eafb

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eafb import MockEafb


def test_atributos_encontrados_eafb():
    m: MagicMock = mock_open(read_data="".join(MockEafb))
    with patch("builtins.open", m):
        n = Eafb.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 4523.0
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_eafb():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Eafb.le_arquivo("")
        assert n.valores is None
        assert n.ree is None


def test_eq_eafb():
    m: MagicMock = mock_open(read_data="".join(MockEafb))
    with patch("builtins.open", m):
        n1 = Eafb.le_arquivo("")
        n2 = Eafb.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
