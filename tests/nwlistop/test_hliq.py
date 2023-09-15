from inewave.nwlistop.hliq import Hliq

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.hliq import MockHliq

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_hliq():
    m: MagicMock = mock_open(read_data="".join(MockHliq))
    with patch("builtins.open", m):
        n = Hliq.read(ARQ_TESTE)
        assert n.usina is not None
        assert n.usina == "CAMARGOS"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2023, 1, 1)
        assert n.valores.iloc[-1, -1] == 12.84


def test_atributos_nao_encontrados_hliq():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Hliq.read(ARQ_TESTE)
        assert n.usina is None
        assert n.valores is None


def test_eq_hliq():
    m: MagicMock = mock_open(read_data="".join(MockHliq))
    with patch("builtins.open", m):
        n1 = Hliq.read(ARQ_TESTE)
        n2 = Hliq.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
