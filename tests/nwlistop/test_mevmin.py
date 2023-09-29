from inewave.nwlistop.mevmin import Mevmin

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.mevmin import MockMevmin

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_mevmin():
    m: MagicMock = mock_open(read_data="".join(MockMevmin))
    with patch("builtins.open", m):
        n = Mevmin.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2020, 1, 1)
        assert n.valores.iloc[-1, -1] == 1114.0
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_mevmin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Mevmin.read(ARQ_TESTE)
        assert n.valores is None
        assert n.ree is None


def test_eq_mevmin():
    m: MagicMock = mock_open(read_data="".join(MockMevmin))
    with patch("builtins.open", m):
        n1 = Mevmin.read(ARQ_TESTE)
        n2 = Mevmin.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
