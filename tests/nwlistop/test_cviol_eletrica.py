from inewave.nwlistop.cviol_eletrica import CviolEletrica

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cviol_eletrica import MockCviolEletrica

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_cviol_eletrica():
    m: MagicMock = mock_open(read_data="".join(MockCviolEletrica))
    with patch("builtins.open", m):
        n = CviolEletrica.read(ARQ_TESTE)
        # Não é possível testar o atributo restricao, pois ele
        # não é escrito no arquivo.
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2021, 1, 1)
        assert n.valores.iloc[5, -1] == 2.8


def test_atributos_nao_encontrados_cviol_eletrica():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = CviolEletrica.read(ARQ_TESTE)
        assert n.restricao is None
        assert n.valores is None


def test_eq_cviol_eletrica():
    m: MagicMock = mock_open(read_data="".join(MockCviolEletrica))
    with patch("builtins.open", m):
        n1 = CviolEletrica.read(ARQ_TESTE)
        n2 = CviolEletrica.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
