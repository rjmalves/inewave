from inewave.nwlistop.dtbmax import Dtbmax

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.dtbmax import MockDtbmax


def test_atributos_encontrados_dtbmax():
    m: MagicMock = mock_open(read_data="".join(MockDtbmax))
    with patch("builtins.open", m):
        n = Dtbmax.le_arquivo("")
        assert n.usina is not None
        assert n.usina == "CAMARGOS"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_dtbmax():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Dtbmax.le_arquivo("")
        assert n.usina is None
        assert n.valores is None


def test_eq_dtbmax():
    m: MagicMock = mock_open(read_data="".join(MockDtbmax))
    with patch("builtins.open", m):
        n1 = Dtbmax.le_arquivo("")
        n2 = Dtbmax.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
