from inewave.nwlistop.merclsin import MerclSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.merclsin import MockMerclSIN

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_merclsin():
    m: MagicMock = mock_open(read_data="".join(MockMerclSIN))
    with patch("builtins.open", m):
        n = MerclSIN.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -2] == 54495.0


def test_atributos_nao_encontrados_merclsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = MerclSIN.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_merclsin():
    m: MagicMock = mock_open(read_data="".join(MockMerclSIN))
    with patch("builtins.open", m):
        n1 = MerclSIN.read(ARQ_TESTE)
        n2 = MerclSIN.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
