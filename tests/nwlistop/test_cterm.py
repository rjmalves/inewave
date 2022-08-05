from inewave.nwlistop.cterm import Cterm

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cterm import MockCterm


def test_atributos_encontrados_cterm():
    m: MagicMock = mock_open(read_data="".join(MockCterm))
    with patch("builtins.open", m):
        n = Cterm.le_arquivo("")
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 585.36


def test_atributos_nao_encontrados_cterm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Cterm.le_arquivo("")
        assert n.submercado is None
        assert n.valores is None


def test_eq_cterm():
    m: MagicMock = mock_open(read_data="".join(MockCterm))
    with patch("builtins.open", m):
        n1 = Cterm.le_arquivo("")
        n2 = Cterm.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
