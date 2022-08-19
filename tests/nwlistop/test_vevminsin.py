from inewave.nwlistop.vevminsin import VevminSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vevminsin import MockVevminSIN


def test_atributos_encontrados_vevminsin():
    m: MagicMock = mock_open(read_data="".join(MockVevminSIN))
    with patch("builtins.open", m):
        n = VevminSIN.le_arquivo("")
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_vevminsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = VevminSIN.le_arquivo("")
        assert n.valores is None


def test_eq_vevminsin():
    m: MagicMock = mock_open(read_data="".join(MockVevminSIN))
    with patch("builtins.open", m):
        n1 = VevminSIN.le_arquivo("")
        n2 = VevminSIN.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
