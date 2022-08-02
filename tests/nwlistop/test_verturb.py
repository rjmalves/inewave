from inewave.nwlistop.verturb import Verturb

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.verturb import MockVerturb


def test_atributos_encontrados_verturb():
    m: MagicMock = mock_open(read_data="".join(MockVerturb))
    with patch("builtins.open", m):
        n = Verturb.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == -2347.0
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_verturb():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Verturb.le_arquivo("")
        assert n.valores is None
        assert n.ree is None


def test_eq_verturb():
    m: MagicMock = mock_open(read_data="".join(MockVerturb))
    with patch("builtins.open", m):
        n1 = Verturb.le_arquivo("")
        n2 = Verturb.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
