from inewave.nwlistop.eaf import Eaf

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eaf import MockEaf

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_eaf():
    m: MagicMock = mock_open(read_data="".join(MockEaf))
    with patch("builtins.open", m):
        n = Eaf.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[-1, -1] == 1401.0
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_eaf():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Eaf.read(ARQ_TESTE)
        assert n.valores is None
        assert n.ree is None


def test_eq_eaf():
    m: MagicMock = mock_open(read_data="".join(MockEaf))
    with patch("builtins.open", m):
        n1 = Eaf.read(ARQ_TESTE)
        n2 = Eaf.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
