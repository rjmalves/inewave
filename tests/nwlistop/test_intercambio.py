from inewave.nwlistop.intercambio import Intercambio

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.intercambio import MockIntercambio

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_intercambio():
    m: MagicMock = mock_open(read_data="".join(MockIntercambio))
    with patch("builtins.open", m):
        n = Intercambio.read(ARQ_TESTE)
        assert n.submercado_de is not None
        assert n.submercado_de == "SUDESTE"
        assert n.submercado_para == "SUL"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2020, 1, 1)
        assert n.valores.iloc[-1, -1] == 2835.2


def test_atributos_nao_encontrados_intercambio():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Intercambio.read(ARQ_TESTE)
        assert n.submercado_de is None
        assert n.submercado_para is None
        assert n.valores is None


def test_eq_intercambio():
    m: MagicMock = mock_open(read_data="".join(MockIntercambio))
    with patch("builtins.open", m):
        n1 = Intercambio.read(ARQ_TESTE)
        n2 = Intercambio.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
