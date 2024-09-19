from datetime import datetime
from unittest.mock import MagicMock, patch

from inewave.nwlistop.cmargmed import Cmargmed
from tests.mocks.arquivos.cmargmed import MockCmargmed, MockCmargmed28
from tests.mocks.mock_open import mock_open

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_cmargmed28():
    m: MagicMock = mock_open(read_data="".join(MockCmargmed28))
    with patch("builtins.open", m):
        Cmargmed.set_version("28")
        n = Cmargmed.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 98.5
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_encontrados_cmargmed():
    m: MagicMock = mock_open(read_data="".join(MockCmargmed))
    with patch("builtins.open", m):
        Cmargmed.set_version("latest")
        n = Cmargmed.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2024, 1, 1)
        assert n.valores.iloc[-1, -1] == 77.30
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_cmargmed():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Cmargmed.read(ARQ_TESTE)
        assert n.valores is None
        assert n.submercado is None


def test_eq_cmargmed():
    m: MagicMock = mock_open(read_data="".join(MockCmargmed))
    with patch("builtins.open", m):
        n1 = Cmargmed.read(ARQ_TESTE)
        n2 = Cmargmed.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
