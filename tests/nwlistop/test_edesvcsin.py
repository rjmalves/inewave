from inewave.nwlistop.edesvcsin import Edesvcsin

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.edesvcsin import MockEdesvcsin

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_edesvcsin():
    m: MagicMock = mock_open(read_data="".join(MockEdesvcsin))
    with patch("builtins.open", m):
        n = Edesvcsin.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2020, 1, 1)
        assert n.valores.iloc[-1, -1] == -654.0


def test_atributos_nao_encontrados_edesvcsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Edesvcsin.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_edesvcsin():
    m: MagicMock = mock_open(read_data="".join(MockEdesvcsin))
    with patch("builtins.open", m):
        n1 = Edesvcsin.read(ARQ_TESTE)
        n2 = Edesvcsin.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
