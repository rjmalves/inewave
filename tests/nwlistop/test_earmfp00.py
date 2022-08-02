from inewave.nwlistop.earmfp00 import Earmfp00

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.earmfp00 import MockEarmfp00


def test_atributos_encontrados_earmfp00():
    m: MagicMock = mock_open(read_data="".join(MockEarmfp00))
    with patch("builtins.open", m):
        n = Earmfp00.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 71.2
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_earmfp00():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Earmfp00.le_arquivo("")
        assert n.valores is None
        assert n.ree is None


def test_eq_earmfp00():
    m: MagicMock = mock_open(read_data="".join(MockEarmfp00))
    with patch("builtins.open", m):
        n1 = Earmfp00.le_arquivo("")
        n2 = Earmfp00.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
