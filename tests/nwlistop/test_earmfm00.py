from inewave.nwlistop.earmfm00 import Earmfm00

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.earmfm00 import MockEarmfm00


def test_atributos_encontrados_earmfm00():
    m: MagicMock = mock_open(read_data="".join(MockEarmfm00))
    with patch("builtins.open", m):
        n = Earmfm00.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 122223.0
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_earmfm00():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Earmfm00.le_arquivo("")
        assert n.valores is None
        assert n.submercado is None


def test_eq_earmfm00():
    m: MagicMock = mock_open(read_data="".join(MockEarmfm00))
    with patch("builtins.open", m):
        n1 = Earmfm00.le_arquivo("")
        n2 = Earmfm00.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
