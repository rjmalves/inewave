from inewave.nwlistop.ghmax_fpha import GhmaxFpha

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghmax_fpha import MockGhmaxFpha

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_ghmax_fpha():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxFpha))
    with patch("builtins.open", m):
        n = GhmaxFpha.read(ARQ_TESTE)
        assert n.usina is not None
        assert n.usina == "FURNAS"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2023, 1, 1)
        assert n.valores.iloc[-1, -1] == 551.05


def test_atributos_nao_encontrados_ghmax_fpha():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = GhmaxFpha.read(ARQ_TESTE)
        assert n.usina is None
        assert n.valores is None


def test_eq_ghmax_fpha():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxFpha))
    with patch("builtins.open", m):
        n1 = GhmaxFpha.read(ARQ_TESTE)
        n2 = GhmaxFpha.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
