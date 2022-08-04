from inewave.nwlistop.ghmaxm import Ghmaxm

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghmaxm import MockGhmaxm


def test_atributos_encontrados_ghmaxm():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxm))
    with patch("builtins.open", m):
        n = Ghmaxm.le_arquivo("")
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 54602.6


def test_atributos_nao_encontrados_ghmaxm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Ghmaxm.le_arquivo("")
        assert n.submercado is None
        assert n.valores is None


def test_eq_ghmaxm():
    m: MagicMock = mock_open(read_data="".join(MockGhmaxm))
    with patch("builtins.open", m):
        n1 = Ghmaxm.le_arquivo("")
        n2 = Ghmaxm.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
