from inewave.nwlistop.custo_futuro import CustoFuturo

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.custo_futuro import MockCustoFuturo

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_custo_futuro():
    m: MagicMock = mock_open(read_data="".join(MockCustoFuturo))
    with patch("builtins.open", m):
        n = CustoFuturo.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 0.3332592e5


def test_atributos_nao_encontrados_custo_futuro():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = CustoFuturo.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_custo_futuro():
    m: MagicMock = mock_open(read_data="".join(MockCustoFuturo))
    with patch("builtins.open", m):
        n1 = CustoFuturo.read(ARQ_TESTE)
        n2 = CustoFuturo.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
