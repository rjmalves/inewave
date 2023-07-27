from inewave.nwlistop.eafm import Eafm

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eafm import MockEafm

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_eafm():
    m: MagicMock = mock_open(read_data="".join(MockEafm))
    with patch("builtins.open", m):
        n = Eafm.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 12836.0
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_eafm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Eafm.read(ARQ_TESTE)
        assert n.valores is None
        assert n.submercado is None


def test_eq_eafm():
    m: MagicMock = mock_open(read_data="".join(MockEafm))
    with patch("builtins.open", m):
        n1 = Eafm.read(ARQ_TESTE)
        n2 = Eafm.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
