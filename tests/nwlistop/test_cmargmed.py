from inewave.nwlistop.cmargmed import CmargMed

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cmargmed import MockCmargMed

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_cmargmed():
    m: MagicMock = mock_open(read_data="".join(MockCmargMed))
    with patch("builtins.open", m):
        n = CmargMed.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 354.22
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_cmargmed():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = CmargMed.read(ARQ_TESTE)
        assert n.valores is None
        assert n.submercado is None


def test_eq_cmargmed():
    m: MagicMock = mock_open(read_data="".join(MockCmargMed))
    with patch("builtins.open", m):
        n1 = CmargMed.read(ARQ_TESTE)
        n2 = CmargMed.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
