from inewave.nwlistop.rhslppdf import RHSLPPdf

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.rhslppdf import MockRHSLPPdf

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_rhslppdf():
    m: MagicMock = mock_open(read_data="".join(MockRHSLPPdf))
    with patch("builtins.open", m):
        n = RHSLPPdf.read(ARQ_TESTE)
        assert n.ree is not None
        assert n.ree == "SUDESTE"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2020
        assert n.valores.iloc[-1, -1] == 0.0


def test_atributos_nao_encontrados_rhslppdf():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = RHSLPPdf.read(ARQ_TESTE)
        assert n.ree is None
        assert n.valores is None


def test_eq_rhslppdf():
    m: MagicMock = mock_open(read_data="".join(MockRHSLPPdf))
    with patch("builtins.open", m):
        n1 = RHSLPPdf.read(ARQ_TESTE)
        n2 = RHSLPPdf.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
