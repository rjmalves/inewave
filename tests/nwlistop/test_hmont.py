from inewave.nwlistop.hmont import Hmont

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.hmont import MockHmont

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_hmont():
    m: MagicMock = mock_open(read_data="".join(MockHmont))
    with patch("builtins.open", m):
        n = Hmont.read(ARQ_TESTE)
        assert n.usina is not None
        assert n.usina == "CAMARGOS"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2023, 1, 1)
        assert n.valores.iloc[-1, -1] == 899.03


def test_atributos_nao_encontrados_hmont():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Hmont.read(ARQ_TESTE)
        assert n.usina is None
        assert n.valores is None


def test_eq_hmont():
    m: MagicMock = mock_open(read_data="".join(MockHmont))
    with patch("builtins.open", m):
        n1 = Hmont.read(ARQ_TESTE)
        n2 = Hmont.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
