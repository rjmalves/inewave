from inewave.nwlistop.depminuh import Depminuh

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.depminuh import MockDepminUH


def test_atributos_encontrados_depminuh():
    m: MagicMock = mock_open(read_data="".join(MockDepminUH))
    with patch("builtins.open", m):
        n = Depminuh.le_arquivo("")
        assert n.usina is not None
        assert n.usina == "CAMARGOS"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 3.57


def test_atributos_nao_encontrados_depminuh():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Depminuh.le_arquivo("")
        assert n.usina is None
        assert n.valores is None


def test_eq_depminuh():
    m: MagicMock = mock_open(read_data="".join(MockDepminUH))
    with patch("builtins.open", m):
        n1 = Depminuh.le_arquivo("")
        n2 = Depminuh.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
