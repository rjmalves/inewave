from inewave.nwlistop.ghtot00 import Ghtot00

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.ghtot00 import MockGhtot00


def test_atributos_encontrados_ghtot00():
    m: MagicMock = mock_open(read_data="".join(MockGhtot00))
    with patch("builtins.open", m):
        n = Ghtot00.le_arquivo("")
        assert n.ree is not None
        assert n.ree == "SUDESTE"
        assert n.geracao is not None
        assert n.geracao.iloc[0, 0] == 2022
        assert n.geracao.iloc[-1, -1] == 2578.7


def test_atributos_nao_encontrados_ghtot00():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Ghtot00.le_arquivo("")
        assert n.ree is None
        assert n.geracao is None


def test_eq_ghtot00():
    m: MagicMock = mock_open(read_data="".join(MockGhtot00))
    with patch("builtins.open", m):
        n1 = Ghtot00.le_arquivo("")
        n2 = Ghtot00.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
