from inewave.nwlistop.earmfpsin import EarmfpSIN

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.earmfpsin import MockEarmfpsin

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_earmfpsin():
    m: MagicMock = mock_open(read_data="".join(MockEarmfpsin))
    with patch("builtins.open", m):
        n = EarmfpSIN.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2021
        assert n.valores.iloc[-1, -1] == 42.1


def test_atributos_nao_encontrados_earmfpsin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = EarmfpSIN.read(ARQ_TESTE)
        assert n.valores is None


def test_eq_earmfpsin():
    m: MagicMock = mock_open(read_data="".join(MockEarmfpsin))
    with patch("builtins.open", m):
        n1 = EarmfpSIN.read(ARQ_TESTE)
        n2 = EarmfpSIN.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
