from inewave.nwlistop.cviol_rhv_sin import CviolRhvsin

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.c_v_rhv_s import MockCVRHVs

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_cviol_rhv_sin():
    m: MagicMock = mock_open(read_data="".join(MockCVRHVs))
    with patch("builtins.open", m):
        n = CviolRhvsin.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2023, 1, 1)
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_cviol_rhv_sin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = CviolRhvsin.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_cviol_rhv_sin():
    m: MagicMock = mock_open(read_data="".join(MockCVRHVs))
    with patch("builtins.open", m):
        n1 = CviolRhvsin.read(ARQ_TESTE)
        n2 = CviolRhvsin.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
