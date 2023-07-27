from inewave.nwlistop.earmf import Earmf

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.earmf import MockEarmf

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_earmf():
    m: MagicMock = mock_open(read_data="".join(MockEarmf))
    with patch("builtins.open", m):
        n = Earmf.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 7639.0
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_earmf():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Earmf.read(ARQ_TESTE)
        assert n.valores is None
        assert n.ree is None


def test_eq_earmf():
    m: MagicMock = mock_open(read_data="".join(MockEarmf))
    with patch("builtins.open", m):
        n1 = Earmf.read(ARQ_TESTE)
        n2 = Earmf.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
