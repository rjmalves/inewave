from inewave.nwlistop.merclsin import MerclSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.merclsin import MockMerclSIN


def test_atributos_encontrados_merclsin():
    m: MagicMock = mock_open(read_data="".join(MockMerclSIN))
    with patch("builtins.open", m):
        n = MerclSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -2] == 56819.0


def test_atributos_nao_encontrados_merclsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = MerclSIN.le_arquivo("")
        assert n.valores is None


def test_eq_merclsin():
    m: MagicMock = mock_open(read_data="".join(MockMerclSIN))
    with patch("builtins.open", m):
        n1 = MerclSIN.le_arquivo("")
        n2 = MerclSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
