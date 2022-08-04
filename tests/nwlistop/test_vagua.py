from inewave.nwlistop.vagua import Vagua

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vagua import MockVagua


def test_atributos_encontrados_vagua():
    m: MagicMock = mock_open(read_data="".join(MockVagua))
    with patch("builtins.open", m):
        n = Vagua.le_arquivo("")
        assert n.ree is not None
        assert n.ree == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == -1.90


def test_atributos_nao_encontrados_vagua():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Vagua.le_arquivo("")
        assert n.ree is None
        assert n.valores is None


def test_eq_vagua():
    m: MagicMock = mock_open(read_data="".join(MockVagua))
    with patch("builtins.open", m):
        n1 = Vagua.le_arquivo("")
        n2 = Vagua.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
