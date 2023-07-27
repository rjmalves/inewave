from inewave.nwlistop.exces import Exces

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.exces import MockExces

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_exces():
    m: MagicMock = mock_open(read_data="".join(MockExces))
    with patch("builtins.open", m):
        n = Exces.read(ARQ_TESTE)
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2020, 1, 1)
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_exces():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Exces.read(ARQ_TESTE)
        assert n.submercado is None
        assert n.valores is None


def test_eq_exces():
    m: MagicMock = mock_open(read_data="".join(MockExces))
    with patch("builtins.open", m):
        n1 = Exces.read(ARQ_TESTE)
        n2 = Exces.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
