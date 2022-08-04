from inewave.nwlistop.ghtotm import Ghtotm

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghtotm import MockGhtotm


def test_atributos_encontrados_ghtotm():
    m: MagicMock = mock_open(read_data="".join(MockGhtotm))
    with patch("builtins.open", m):
        n = Ghtotm.le_arquivo("")
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 24494.9


def test_atributos_nao_encontrados_ghtotm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Ghtotm.le_arquivo("")
        assert n.submercado is None
        assert n.valores is None


def test_eq_ghtotm():
    m: MagicMock = mock_open(read_data="".join(MockGhtotm))
    with patch("builtins.open", m):
        n1 = Ghtotm.le_arquivo("")
        n2 = Ghtotm.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
