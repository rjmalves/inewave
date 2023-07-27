from inewave.nwlistop.evertm import Evertm

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.evertm import MockEvertm

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_evertm():
    m: MagicMock = mock_open(read_data="".join(MockEvertm))
    with patch("builtins.open", m):
        n = Evertm.read(ARQ_TESTE)
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2020, 1, 1)
        assert n.valores.iloc[-1, -1] == 233.0


def test_atributos_nao_encontrados_evertm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Evertm.read(ARQ_TESTE)
        assert n.submercado is None
        assert n.valores is None


def test_eq_evertm():
    m: MagicMock = mock_open(read_data="".join(MockEvertm))
    with patch("builtins.open", m):
        n1 = Evertm.read(ARQ_TESTE)
        n2 = Evertm.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
