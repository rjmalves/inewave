from inewave.nwlistop.gttot import Gttot

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.gttot import MockGttot

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_gttot():
    m: MagicMock = mock_open(read_data="".join(MockGttot))
    with patch("builtins.open", m):
        n = Gttot.read(ARQ_TESTE)
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2022, 1, 1)
        assert n.valores.iloc[-1, -1] == 2853.5


def test_atributos_nao_encontrados_gttot():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Gttot.read(ARQ_TESTE)
        assert n.submercado is None
        assert n.valores is None


def test_eq_gttot():
    m: MagicMock = mock_open(read_data="".join(MockGttot))
    with patch("builtins.open", m):
        n1 = Gttot.read(ARQ_TESTE)
        n2 = Gttot.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
