from inewave.nwlistcf import Nwlistcfrel

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.nwlistcfrel import MockNwlistcfrel

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_nwlistcfrel():
    m: MagicMock = mock_open(read_data="".join(MockNwlistcfrel))
    with patch("builtins.open", m):
        n = Nwlistcfrel.read(ARQ_TESTE)
        assert n.cortes is not None


def test_atributos_nao_encontrados_nwlistcfrel():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Nwlistcfrel.read(ARQ_TESTE)
        assert n.cortes is None


def test_eq_nwlistcfrel():
    m: MagicMock = mock_open(read_data="".join(MockNwlistcfrel))
    with patch("builtins.open", m):
        n1 = Nwlistcfrel.read(ARQ_TESTE)
        n2 = Nwlistcfrel.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
