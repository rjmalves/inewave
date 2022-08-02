from inewave.nwlistop.eafbsin import EafbSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eafbsin import MockEafbSIN


def test_atributos_encontrados_eafbsin():
    m: MagicMock = mock_open(read_data="".join(MockEafbSIN))
    with patch("builtins.open", m):
        n = EafbSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 64920.0


def test_atributos_nao_encontrados_eafbsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = EafbSIN.le_arquivo("")
        assert n.valores is None


def test_eq_eafbsin():
    m: MagicMock = mock_open(read_data="".join(MockEafbSIN))
    with patch("builtins.open", m):
        n1 = EafbSIN.le_arquivo("")
        n2 = EafbSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
