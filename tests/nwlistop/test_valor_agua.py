from inewave.nwlistop.valor_agua import ValorAgua

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vagua import MockVagua

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_valor_agua():
    m: MagicMock = mock_open(read_data="".join(MockVagua))
    with patch("builtins.open", m):
        n = ValorAgua.read(ARQ_TESTE)
        assert n.ree is not None
        assert n.ree == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2022, 1, 1)
        assert n.valores.iloc[-1, -1] == -0.09


def test_atributos_nao_encontrados_valor_agua():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = ValorAgua.read(ARQ_TESTE)
        assert n.ree is None
        assert n.valores is None


def test_eq_valor_agua():
    m: MagicMock = mock_open(read_data="".join(MockVagua))
    with patch("builtins.open", m):
        n1 = ValorAgua.read(ARQ_TESTE)
        n2 = ValorAgua.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
