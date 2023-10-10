from inewave.nwlistop.cbomb import Cbomb

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cbomb import MockCbomb

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_cbomb():
    m: MagicMock = mock_open(read_data="".join(MockCbomb))
    with patch("builtins.open", m):
        n = Cbomb.read(ARQ_TESTE)
        assert n.estacao is not None
        assert n.estacao == "Sta Cecilia"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2023, 1, 1)
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_cbomb():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Cbomb.read(ARQ_TESTE)
        assert n.estacao is None
        assert n.valores is None


def test_eq_cbomb():
    m: MagicMock = mock_open(read_data="".join(MockCbomb))
    with patch("builtins.open", m):
        n1 = Cbomb.read(ARQ_TESTE)
        n2 = Cbomb.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
