from inewave.nwlistop.mercl import Mercl

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.mercl import MockMercl


def test_atributos_encontrados_mercl():
    m: MagicMock = mock_open(read_data="".join(MockMercl))
    with patch("builtins.open", m):
        n = Mercl.le_arquivo("")
        assert n.valores is not None
        print(n.valores)
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -2] == 37783.0
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_mercl():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Mercl.le_arquivo("")
        assert n.valores is None
        assert n.submercado is None


def test_eq_mercl():
    m: MagicMock = mock_open(read_data="".join(MockMercl))
    with patch("builtins.open", m):
        n1 = Mercl.le_arquivo("")
        n2 = Mercl.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
