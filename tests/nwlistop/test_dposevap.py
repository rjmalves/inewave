from inewave.nwlistop.dposevap import Dposevap

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.dpos_evap import MockDposEvap

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_dposevap():
    m: MagicMock = mock_open(read_data="".join(MockDposEvap))
    with patch("builtins.open", m):
        n = Dposevap.read(ARQ_TESTE)
        assert n.usina is not None
        assert n.usina == "FURNAS"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2023, 1, 1)
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_dposevap():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Dposevap.read(ARQ_TESTE)
        assert n.usina is None
        assert n.valores is None


def test_eq_dposevap():
    m: MagicMock = mock_open(read_data="".join(MockDposEvap))
    with patch("builtins.open", m):
        n1 = Dposevap.read(ARQ_TESTE)
        n2 = Dposevap.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
