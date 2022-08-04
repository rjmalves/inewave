from inewave.nwlistop.ghmaxmr import Ghmaxmr

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghmaxmr import MockGhmaxmr


def test_atributos_encontrados_ghmaxmr():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxmr))
    with patch("builtins.open", m):
        n = Ghmaxmr.le_arquivo("")
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 54233.6


def test_atributos_nao_encontrados_ghmaxmr():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Ghmaxmr.le_arquivo("")
        assert n.submercado is None
        assert n.valores is None


def test_eq_ghmaxmr():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxmr))
    with patch("builtins.open", m):
        n1 = Ghmaxmr.le_arquivo("")
        n2 = Ghmaxmr.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
