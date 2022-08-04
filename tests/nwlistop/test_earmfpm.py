from inewave.nwlistop.earmfpm import Earmfpm

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.earmfpm import MockEarmfpm


def test_atributos_encontrados_earmfpm():
    m: MagicMock = mock_open(read_data="".join(MockEarmfpm))
    with patch("builtins.open", m):
        n = Earmfpm.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 1995
        assert n.valores.iloc[-1, -1] == 63.0
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_earmfpm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Earmfpm.le_arquivo("")
        assert n.valores is None
        assert n.submercado is None


def test_eq_earmfpm():
    m: MagicMock = mock_open(read_data="".join(MockEarmfpm))
    with patch("builtins.open", m):
        n1 = Earmfpm.le_arquivo("")
        n2 = Earmfpm.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
