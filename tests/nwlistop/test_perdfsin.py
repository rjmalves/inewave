from inewave.nwlistop.perdfsin import PerdfSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.perdfsin import MockPerdfSIN


def test_atributos_encontrados_perdfsin():
    m: MagicMock = mock_open(read_data="".join(MockPerdfSIN))
    with patch("builtins.open", m):
        n = PerdfSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 438.0


def test_atributos_nao_encontrados_perdfsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = PerdfSIN.le_arquivo("")
        assert n.valores is None


def test_eq_perdfsin():
    m: MagicMock = mock_open(read_data="".join(MockPerdfSIN))
    with patch("builtins.open", m):
        n1 = PerdfSIN.le_arquivo("")
        n2 = PerdfSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
