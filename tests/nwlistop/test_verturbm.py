from inewave.nwlistop.verturbm import Verturbm

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.verturbm import MockVerturbm


def test_atributos_encontrados_verturbm():
    m: MagicMock = mock_open(read_data="".join(MockVerturbm))
    with patch("builtins.open", m):
        n = Verturbm.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 0.0
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_verturbm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Verturbm.le_arquivo("")
        assert n.valores is None
        assert n.submercado is None


def test_eq_verturbm():
    m: MagicMock = mock_open(read_data="".join(MockVerturbm))
    with patch("builtins.open", m):
        n1 = Verturbm.le_arquivo("")
        n2 = Verturbm.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
