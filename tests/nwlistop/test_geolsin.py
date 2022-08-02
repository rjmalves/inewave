from inewave.nwlistop.geolsin import GeolSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.geolsin import MockGeolSIN


def test_atributos_encontrados_geolsin():
    m: MagicMock = mock_open(read_data="".join(MockGeolSIN))
    with patch("builtins.open", m):
        n = GeolSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 6574.3


def test_atributos_nao_encontrados_geolsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = GeolSIN.le_arquivo("")
        assert n.valores is None


def test_eq_geolsin():
    m: MagicMock = mock_open(read_data="".join(MockGeolSIN))
    with patch("builtins.open", m):
        n1 = GeolSIN.le_arquivo("")
        n2 = GeolSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
