from inewave.nwlistop.geolsin import Geolsin

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.geolsin import MockGeolSIN

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_geolsin():
    m: MagicMock = mock_open(read_data="".join(MockGeolSIN))
    with patch("builtins.open", m):
        n = Geolsin.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 6721.6


def test_atributos_nao_encontrados_geolsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Geolsin.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_geolsin():
    m: MagicMock = mock_open(read_data="".join(MockGeolSIN))
    with patch("builtins.open", m):
        n1 = Geolsin.read(ARQ_TESTE)
        n2 = Geolsin.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
