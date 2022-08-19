from inewave.nwlistop.vevminm import Vevminm

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vevminm import MockVevminm


def test_atributos_encontrados_vevminm():
    m: MagicMock = mock_open(read_data="".join(MockVevminm))
    with patch("builtins.open", m):
        n = Vevminm.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 0.0
        assert n.submercado is not None
        assert n.submercado == "SUDESTE"


def test_atributos_nao_encontrados_vevminm():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Vevminm.le_arquivo("")
        assert n.valores is None
        assert n.submercado is None


def test_eq_vevminm():
    m: MagicMock = mock_open(read_data="".join(MockVevminm))
    with patch("builtins.open", m):
        n1 = Vevminm.le_arquivo("")
        n2 = Vevminm.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
