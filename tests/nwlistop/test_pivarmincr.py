from datetime import datetime
from unittest.mock import MagicMock, patch

from inewave.nwlistop.pivarmincr import Pivarmincr
from tests.mocks.mock_open import mock_open
from tests.mocks.arquivos.pivarmincr import (
    MockPivarmincr,
    MockPivarmincr_v29_2,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_pivarmincr():
    m: MagicMock = mock_open(read_data="".join(MockPivarmincr))
    with patch("builtins.open", m):
        n = Pivarmincr.read(ARQ_TESTE, version="28.12")
        assert n.usina == "FURNAS"
        assert n.valores.iloc[0, 0] == datetime(2023, 1, 1)
        assert n.valores.iloc[3, -1] == 0.49
        assert n.valores.iloc[-1, -1] == 0.89


def test_atributos_encontrados_pivarmincr_v29_2():
    m: MagicMock = mock_open(read_data="".join(MockPivarmincr_v29_2))
    with patch("builtins.open", m):
        n = Pivarmincr.read(ARQ_TESTE, version="29.2")
        assert n.usina == "FURNAS"
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[3, -1] == -312253.4
        assert n.valores.iloc[-1, -1] == -418673.9


def test_atributos_nao_encontrados_pivarmincr():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Pivarmincr.read(ARQ_TESTE)
        assert n.usina is None and n.valores is None


def test_eq_pivarmincr():
    m: MagicMock = mock_open(read_data="".join(MockPivarmincr))
    with patch("builtins.open", m):
        n1 = Pivarmincr.read(ARQ_TESTE)
        n2 = Pivarmincr.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
