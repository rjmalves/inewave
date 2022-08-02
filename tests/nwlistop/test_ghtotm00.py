from inewave.nwlistop.ghtotm00 import Ghtotm00

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghtotm00 import MockGhtotm00


def test_atributos_encontrados_ghtotm00():
    m: MagicMock = mock_open(read_data="".join(MockGhtotm00))
    with patch("builtins.open", m):
        n = Ghtotm00.le_arquivo("")
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 24494.9


def test_atributos_nao_encontrados_ghtotm00():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Ghtotm00.le_arquivo("")
        assert n.submercado is None
        assert n.valores is None


def test_eq_ghtotm00():
    m: MagicMock = mock_open(read_data="".join(MockGhtotm00))
    with patch("builtins.open", m):
        n1 = Ghtotm00.le_arquivo("")
        n2 = Ghtotm00.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
