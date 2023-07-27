from inewave.nwlistop.ghtotsin import GhtotSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghtotsin import MockGhtotsin

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_ghtotsin():
    m: MagicMock = mock_open(read_data="".join(MockGhtotsin))
    with patch("builtins.open", m):
        n = GhtotSIN.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 49211.7


def test_atributos_nao_encontrados_ghtotsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = GhtotSIN.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_ghtotsin():
    m: MagicMock = mock_open(read_data="".join(MockGhtotsin))
    with patch("builtins.open", m):
        n1 = GhtotSIN.read(ARQ_TESTE)
        n2 = GhtotSIN.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
