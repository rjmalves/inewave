from inewave.nwlistop.viol_neg_evap import ViolNegEvap

import numpy as np
from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.dneg_evap import MockDnegEvap

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_viol_neg_evap():
    m: MagicMock = mock_open(read_data="".join(MockDnegEvap))
    with patch("builtins.open", m):
        n = ViolNegEvap.read(ARQ_TESTE)
        assert n.usina is not None
        assert n.usina == "SAO ROQUE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2023, 1, 1)
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_viol_neg_evap():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = ViolNegEvap.read(ARQ_TESTE)
        assert n.usina is None
        assert n.valores is None


def test_eq_viol_neg_evap():
    m: MagicMock = mock_open(read_data="".join(MockDnegEvap))
    with patch("builtins.open", m):
        n1 = ViolNegEvap.read(ARQ_TESTE)
        n2 = ViolNegEvap.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
