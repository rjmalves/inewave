from inewave.nwlistop.ctermsin import Ctermsin

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ctermsin import MockCtermSIN

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_ctermsin():
    m: MagicMock = mock_open(read_data="".join(MockCtermSIN))
    with patch("builtins.open", m):
        n = Ctermsin.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 1581.41


def test_atributos_nao_encontrados_ctermsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Ctermsin.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_ctermsin():
    m: MagicMock = mock_open(read_data="".join(MockCtermSIN))
    with patch("builtins.open", m):
        n1 = Ctermsin.read(ARQ_TESTE)
        n2 = Ctermsin.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
