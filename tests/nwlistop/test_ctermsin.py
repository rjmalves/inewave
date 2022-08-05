from inewave.nwlistop.ctermsin import CtermSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ctermsin import MockCtermSIN


def test_atributos_encontrados_ctermsin():
    m: MagicMock = mock_open(read_data="".join(MockCtermSIN))
    with patch("builtins.open", m):
        n = CtermSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 1230.35


def test_atributos_nao_encontrados_ctermsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = CtermSIN.le_arquivo("")
        assert n.valores is None


def test_eq_ctermsin():
    m: MagicMock = mock_open(read_data="".join(MockCtermSIN))
    with patch("builtins.open", m):
        n1 = CtermSIN.le_arquivo("")
        n2 = CtermSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
