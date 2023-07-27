from inewave.nwlistop.geolm import Geolm

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.geolm import MockGeolm

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_geolm():
    m: MagicMock = mock_open(read_data="".join(MockGeolm))
    with patch("builtins.open", m):
        n = Geolm.read(ARQ_TESTE)
        assert n.submercado is not None
        assert n.submercado == "NORDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 5964.8


def test_atributos_nao_encontrados_geolm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Geolm.read(ARQ_TESTE)
        assert n.submercado is None
        assert n.valores is None


def test_eq_geolm():
    m: MagicMock = mock_open(read_data="".join(MockGeolm))
    with patch("builtins.open", m):
        n1 = Geolm.read(ARQ_TESTE)
        n2 = Geolm.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
