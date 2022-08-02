from inewave.nwlistop.eafb00 import Eafb00

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eafb00 import MockEafb00


def test_atributos_encontrados_eafb00():
    m: MagicMock = mock_open(read_data="".join(MockEafb00))
    with patch("builtins.open", m):
        n = Eafb00.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 4523.0
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_eafb00():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Eafb00.le_arquivo("")
        assert n.valores is None
        assert n.ree is None


def test_eq_eafb00():
    m: MagicMock = mock_open(read_data="".join(MockEafb00))
    with patch("builtins.open", m):
        n1 = Eafb00.le_arquivo("")
        n2 = Eafb00.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
