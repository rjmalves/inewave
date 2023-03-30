from inewave.nwlistop.corteolm import Corteolm

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.corteolm import MockCorteolm


def test_atributos_encontrados_corteolm():
    m: MagicMock = mock_open(read_data="".join(MockCorteolm))
    with patch("builtins.open", m):
        n = Corteolm.le_arquivo("")
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_corteolm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Corteolm.le_arquivo("")
        assert n.submercado is None
        assert n.valores is None


def test_eq_corteolm():
    m: MagicMock = mock_open(read_data="".join(MockCorteolm))
    with patch("builtins.open", m):
        n1 = Corteolm.le_arquivo("")
        n2 = Corteolm.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
