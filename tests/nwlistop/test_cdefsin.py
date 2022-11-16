from inewave.nwlistop.cdefsin import CdefSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cdefsin import MockCdefSIN


def test_atributos_encontrados_cdefsin():
    m: MagicMock = mock_open(read_data="".join(MockCdefSIN))
    with patch("builtins.open", m):
        n = CdefSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_cdefsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = CdefSIN.le_arquivo("")
        assert n.valores is None


def test_eq_cdefsin():
    m: MagicMock = mock_open(read_data="".join(MockCdefSIN))
    with patch("builtins.open", m):
        n1 = CdefSIN.le_arquivo("")
        n2 = CdefSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
