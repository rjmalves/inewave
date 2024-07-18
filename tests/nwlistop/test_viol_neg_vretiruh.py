from inewave.nwlistop.viol_neg_vretiruh import ViolNegVretiruh

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.viol_neg_vretiruh import MockViolNegVretiruh

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_viol_neg_vretiruh():
    m: MagicMock = mock_open(read_data="".join(MockViolNegVretiruh))
    with patch("builtins.open", m):
        n = ViolNegVretiruh.read(ARQ_TESTE)
        assert n.usina == "CAMARGOS"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_viol_neg_vretiruh():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = ViolNegVretiruh.read(ARQ_TESTE)
        assert n.usina is None
        assert n.valores is None


def test_eq_viol_neg_vretiruh():
    m: MagicMock = mock_open(read_data="".join(MockViolNegVretiruh))
    with patch("builtins.open", m):
        n1 = ViolNegVretiruh.read(ARQ_TESTE)
        n2 = ViolNegVretiruh.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
