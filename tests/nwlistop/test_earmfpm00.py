from inewave.nwlistop.earmfpm00 import Earmfpm00

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.earmfpm00 import MockEarmfpm00


def test_atributos_encontrados_earmfpm00():
    m: MagicMock = mock_open(read_data="".join(MockEarmfpm00))
    with patch("builtins.open", m):
        n = Earmfpm00.le_arquivo("")
        assert n.energias is not None
        assert n.energias.iloc[0, 0] == 1995
        assert n.energias.iloc[-1, -1] == 63.0
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_earmfpm00():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Earmfpm00.le_arquivo("")
        assert n.energias is None
        assert n.submercado is None


def test_eq_earmfpm00():
    m: MagicMock = mock_open(read_data="".join(MockEarmfpm00))
    with patch("builtins.open", m):
        n1 = Earmfpm00.le_arquivo("")
        n2 = Earmfpm00.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
