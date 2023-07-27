from inewave.nwlistop.vevmin import Vevmin

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vevmin import MockVevmin

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_vevmin():
    m: MagicMock = mock_open(read_data="".join(MockVevmin))
    with patch("builtins.open", m):
        n = Vevmin.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2020, 1, 1)
        assert n.valores.iloc[-1, -1] == 0.0
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_vevmin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Vevmin.read(ARQ_TESTE)
        assert n.valores is None
        assert n.ree is None


def test_eq_vevmin():
    m: MagicMock = mock_open(read_data="".join(MockVevmin))
    with patch("builtins.open", m):
        n1 = Vevmin.read(ARQ_TESTE)
        n2 = Vevmin.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
