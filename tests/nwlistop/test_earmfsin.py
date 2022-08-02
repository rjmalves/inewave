from inewave.nwlistop.earmfsin import EarmfSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.earmfsin import MockEarmfSIN


def test_atributos_encontrados_earmfsin():
    m: MagicMock = mock_open(read_data="".join(MockEarmfSIN))
    with patch("builtins.open", m):
        n = EarmfSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 177927.0


def test_atributos_nao_encontrados_earmfsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = EarmfSIN.le_arquivo("")
        assert n.valores is None


def test_eq_earmfsin():
    m: MagicMock = mock_open(read_data="".join(MockEarmfSIN))
    with patch("builtins.open", m):
        n1 = EarmfSIN.le_arquivo("")
        n2 = EarmfSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
