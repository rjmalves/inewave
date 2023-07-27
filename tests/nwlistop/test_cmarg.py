from inewave.nwlistop.cmarg import Cmarg

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cmarg import MockCmarg

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_cmarg():
    m: MagicMock = mock_open(read_data="".join(MockCmarg))
    with patch("builtins.open", m):
        n = Cmarg.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(1995, 1, 1)
        assert n.valores.iloc[-1, -1] == 16.61
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_cmarg():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Cmarg.read(ARQ_TESTE)
        assert n.valores is None
        assert n.submercado is None


def test_eq_cmarg():
    m: MagicMock = mock_open(read_data="".join(MockCmarg))
    with patch("builtins.open", m):
        n1 = Cmarg.read(ARQ_TESTE)
        n2 = Cmarg.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
