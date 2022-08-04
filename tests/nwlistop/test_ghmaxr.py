from inewave.nwlistop.ghmaxr import Ghmaxr

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghmaxr import MockGhmaxr


def test_atributos_encontrados_ghmaxr():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxr))
    with patch("builtins.open", m):
        n = Ghmaxr.le_arquivo("")
        assert n.ree is not None
        assert n.ree == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 7686.3


def test_atributos_nao_encontrados_ghmaxr():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Ghmaxr.le_arquivo("")
        assert n.ree is None
        assert n.valores is None


def test_eq_ghmaxr():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxr))
    with patch("builtins.open", m):
        n1 = Ghmaxr.le_arquivo("")
        n2 = Ghmaxr.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
