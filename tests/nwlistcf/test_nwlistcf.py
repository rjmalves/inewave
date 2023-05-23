from inewave.nwlistcf import Nwlistcf

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.nwlistcf import MockNwlistcf

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_nwlistcf():
    m: MagicMock = mock_open(read_data="".join(MockNwlistcf))
    with patch("builtins.open", m):
        n = Nwlistcf.read(ARQ_TESTE)
        assert n.cortes is not None


def test_atributos_nao_encontrados_nwlistcf():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Nwlistcf.read(ARQ_TESTE)
        assert n.cortes is None


def test_eq_nwlistcf():
    m: MagicMock = mock_open(read_data="".join(MockNwlistcf))
    with patch("builtins.open", m):
        n1 = Nwlistcf.read(ARQ_TESTE)
        n2 = Nwlistcf.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
