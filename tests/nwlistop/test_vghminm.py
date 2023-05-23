from inewave.nwlistop.vghminm import Vghminm

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vghminm import MockVghminm

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_vghminm():
    m: MagicMock = mock_open(read_data="".join(MockVghminm))
    with patch("builtins.open", m):
        n = Vghminm.read(ARQ_TESTE)
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_vghminm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Vghminm.read(ARQ_TESTE)
        assert n.submercado is None
        assert n.valores is None


def test_eq_vghminm():
    m: MagicMock = mock_open(read_data="".join(MockVghminm))
    with patch("builtins.open", m):
        n1 = Vghminm.read(ARQ_TESTE)
        n2 = Vghminm.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
