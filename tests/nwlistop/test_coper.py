from inewave.nwlistop.coper import Coper

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.coper import MockCoper

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_coper():
    m: MagicMock = mock_open(read_data="".join(MockCoper))
    with patch("builtins.open", m):
        n = Coper.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2022, 1, 1)
        assert n.valores.iloc[-1, -1] == 691.64


def test_atributos_nao_encontrados_coper():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Coper.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_coper():
    m: MagicMock = mock_open(read_data="".join(MockCoper))
    with patch("builtins.open", m):
        n1 = Coper.read(ARQ_TESTE)
        n2 = Coper.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
