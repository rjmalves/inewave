from inewave.nwlistop.vturuh import VturUH

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vturuh import MockVturUH


def test_atributos_encontrados_vturuh():
    m: MagicMock = mock_open(read_data="".join(MockVturUH))
    with patch("builtins.open", m):
        n = VturUH.le_arquivo("")
        assert n.usina is not None
        assert n.usina == "CAMARGOS"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 98.77


def test_atributos_nao_encontrados_vturuh():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = VturUH.le_arquivo("")
        assert n.usina is None
        assert n.valores is None


def test_eq_vturuh():
    m: MagicMock = mock_open(read_data="".join(MockVturUH))
    with patch("builtins.open", m):
        n1 = VturUH.le_arquivo("")
        n2 = VturUH.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
