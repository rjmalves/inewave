from inewave.nwlistop.ghmaxrsin import GhmaxrSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghmaxrsin import MockGhmaxrSIN


def test_atributos_encontrados_ghmaxrsin():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxrSIN))
    with patch("builtins.open", m):
        n = GhmaxrSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 94172.9


def test_atributos_nao_encontrados_ghmaxrsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = GhmaxrSIN.le_arquivo("")
        assert n.valores is None


def test_eq_ghmaxrsin():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxrSIN))
    with patch("builtins.open", m):
        n1 = GhmaxrSIN.le_arquivo("")
        n2 = GhmaxrSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
