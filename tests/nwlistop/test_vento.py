from inewave.nwlistop.vento import Vento

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vento import MockVento


def test_atributos_encontrados_vento():
    m: MagicMock = mock_open(read_data="".join(MockVento))
    with patch("builtins.open", m):
        n = Vento.le_arquivo("")
        assert n.usina is not None
        # assert n.usina == "cluster_NE_1"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 7.8825


def test_atributos_nao_encontrados_vento():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Vento.le_arquivo("")
        assert n.usina is None
        assert n.valores is None


def test_eq_vento():
    m: MagicMock = mock_open(read_data="".join(MockVento))
    with patch("builtins.open", m):
        n1 = Vento.le_arquivo("")
        n2 = Vento.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
