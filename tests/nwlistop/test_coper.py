from inewave.nwlistop.coper import Coper

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.coper import MockCoper


def test_atributos_encontrados_coper():
    m: MagicMock = mock_open(read_data="".join(MockCoper))
    with patch("builtins.open", m):
        n = Coper.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 1155.67


def test_atributos_nao_encontrados_coper():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Coper.le_arquivo("")
        assert n.valores is None


def test_eq_coper():
    m: MagicMock = mock_open(read_data="".join(MockCoper))
    with patch("builtins.open", m):
        n1 = Coper.le_arquivo("")
        n2 = Coper.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
