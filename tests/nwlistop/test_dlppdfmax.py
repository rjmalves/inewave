from inewave.nwlistop.dlppdfmax import DLPPdfmax

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.dlppdfmax import MockDLPPdfmax


def test_atributos_encontrados_dlppdfmax():
    m: MagicMock = mock_open(read_data="".join(MockDLPPdfmax))
    with patch("builtins.open", m):
        n = DLPPdfmax.le_arquivo("")
        assert n.ree is not None
        assert n.ree == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_dlppdfmax():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = DLPPdfmax.le_arquivo("")
        assert n.ree is None
        assert n.valores is None


def test_eq_dlppdfmax():
    m: MagicMock = mock_open(read_data="".join(MockDLPPdfmax))
    with patch("builtins.open", m):
        n1 = DLPPdfmax.le_arquivo("")
        n2 = DLPPdfmax.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
