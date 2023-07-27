from inewave.nwlistop.eafbm import Eafbm

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eafbm import MockEafbm

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_eafbm():
    m: MagicMock = mock_open(read_data="".join(MockEafbm))
    with patch("builtins.open", m):
        n = Eafbm.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(1995, 1, 1)
        assert n.valores.iloc[-1, -1] == 28024.0
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_eafbm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Eafbm.read(ARQ_TESTE)
        assert n.valores is None
        assert n.submercado is None


def test_eq_eafbm():
    m: MagicMock = mock_open(read_data="".join(MockEafbm))
    with patch("builtins.open", m):
        n1 = Eafbm.read(ARQ_TESTE)
        n2 = Eafbm.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
