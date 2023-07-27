from inewave.nwlistop.geol import Geol

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.geol import MockGeol

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_geol():
    m: MagicMock = mock_open(read_data="".join(MockGeol))
    with patch("builtins.open", m):
        n = Geol.read(ARQ_TESTE)
        assert n.usina is not None
        # assert n.pee == "cluster_NE_1"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 2875.5


def test_atributos_nao_encontrados_geol():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Geol.read(ARQ_TESTE)
        assert n.usina is None
        assert n.valores is None


def test_eq_geol():
    m: MagicMock = mock_open(read_data="".join(MockGeol))
    with patch("builtins.open", m):
        n1 = Geol.read(ARQ_TESTE)
        n2 = Geol.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
