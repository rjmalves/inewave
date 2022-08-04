from inewave.nwlistop.cmargmed import CmargMed

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cmargmed import MockCmargMed


def test_atributos_encontrados_cmargmed():
    m: MagicMock = mock_open(read_data="".join(MockCmargMed))
    with patch("builtins.open", m):
        n = CmargMed.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 354.22
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_cmargmed():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = CmargMed.le_arquivo("")
        assert n.valores is None
        assert n.submercado is None


def test_eq_cmargmed():
    m: MagicMock = mock_open(read_data="".join(MockCmargMed))
    with patch("builtins.open", m):
        n1 = CmargMed.le_arquivo("")
        n2 = CmargMed.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
