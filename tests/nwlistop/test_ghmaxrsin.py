from inewave.nwlistop.ghmaxrsin import GhmaxrSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghmaxrsin import MockGhmaxrSIN

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_ghmaxrsin():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxrSIN))
    with patch("builtins.open", m):
        n = GhmaxrSIN.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 94172.9


def test_atributos_nao_encontrados_ghmaxrsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = GhmaxrSIN.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_ghmaxrsin():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxrSIN))
    with patch("builtins.open", m):
        n1 = GhmaxrSIN.read(ARQ_TESTE)
        n2 = GhmaxrSIN.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
