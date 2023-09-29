from inewave.nwlistop.ghidrsin import Ghidrsin

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghidrsin import MockGhidrsin

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_ghidrsin():
    m: MagicMock = mock_open(read_data="".join(MockGhidrsin))
    with patch("builtins.open", m):
        n = Ghidrsin.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2020, 1, 1)
        assert n.valores.iloc[-1, -1] == 25070.1


def test_atributos_nao_encontrados_ghidrsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Ghidrsin.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_ghidrsin():
    m: MagicMock = mock_open(read_data="".join(MockGhidrsin))
    with patch("builtins.open", m):
        n1 = Ghidrsin.read(ARQ_TESTE)
        n2 = Ghidrsin.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
