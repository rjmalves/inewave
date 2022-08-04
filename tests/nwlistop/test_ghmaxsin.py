from inewave.nwlistop.ghmaxsin import GhmaxSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghmaxsin import MockGhmaxSIN


def test_atributos_encontrados_ghmaxsin():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxSIN))
    with patch("builtins.open", m):
        n = GhmaxSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 97716.9


def test_atributos_nao_encontrados_ghmaxsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = GhmaxSIN.le_arquivo("")
        assert n.valores is None


def test_eq_ghmaxsin():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxSIN))
    with patch("builtins.open", m):
        n1 = GhmaxSIN.le_arquivo("")
        n2 = GhmaxSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
