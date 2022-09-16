from inewave.nwlistop.earmf import Earmf

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.earmf import MockEarmf


def test_atributos_encontrados_earmf():
    m: MagicMock = mock_open(read_data="".join(MockEarmf))
    with patch("builtins.open", m):
        n = Earmf.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 20770.0
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_earmf():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Earmf.le_arquivo("")
        assert n.valores is None
        assert n.ree is None


def test_eq_earmf():
    m: MagicMock = mock_open(read_data="".join(MockEarmf))
    with patch("builtins.open", m):
        n1 = Earmf.le_arquivo("")
        n2 = Earmf.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
