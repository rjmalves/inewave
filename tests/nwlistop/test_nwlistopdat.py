from inewave.nwlistop.nwlistopdat import Nwlistopdat

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.nwlistopdat import (
    MockNwlistopdatOp1,
    MockNwlistopdatOp2,
    MockNwlistopdatOp4,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_nwlistopdat_op1():
    m: MagicMock = mock_open(read_data="".join(MockNwlistopdatOp1))
    with patch("builtins.open", m):
        n = Nwlistopdat.read(ARQ_TESTE)
        assert n.periodo_inicial_impressao == 1
        assert n.periodo_final_impressao == 1
        assert n.serie_inicial_impressao == 1
        assert n.serie_final_impressao == 1


def test_eq_nwlistopdat_op1():
    m: MagicMock = mock_open(read_data="".join(MockNwlistopdatOp1))
    with patch("builtins.open", m):
        n1 = Nwlistopdat.read(ARQ_TESTE)
        n2 = Nwlistopdat.read(ARQ_TESTE)
        assert n1 == n2


def test_neq_nwlistopdat_op1():
    m: MagicMock = mock_open(read_data="".join(MockNwlistopdatOp1))
    with patch("builtins.open", m):
        n1 = Nwlistopdat.read(ARQ_TESTE)
        n2 = Nwlistopdat.read(ARQ_TESTE)
        n1.periodo_inicial_impressao = 49
        assert n1 != n2
        n1.periodo_inicial_impressao = 1
        n1.periodo_final_impressao = 49
        assert n1 != n2
        n1.periodo_final_impressao = 1
        n1.serie_inicial_impressao = 10
        assert n1 != n2
        n1.serie_inicial_impressao = 1
        n1.serie_final_impressao = 20
        assert n1 != n2


def test_atributos_encontrados_nwlistopdat_op2():
    m: MagicMock = mock_open(read_data="".join(MockNwlistopdatOp2))
    with patch("builtins.open", m):
        n = Nwlistopdat.read(ARQ_TESTE)
        assert n.periodo_inicial_impressao == 1
        assert n.periodo_final_impressao == 58
        assert n.variaveis_impressao_estagios_agregados[0] == 99
        assert n.variaveis_impressao_estagios_individualizados[0] == 99
        assert n.uhes_impressao_estagios_individualizados[0] == 999


def test_eq_nwlistopdat_op2():
    m: MagicMock = mock_open(read_data="".join(MockNwlistopdatOp2))
    with patch("builtins.open", m):
        n1 = Nwlistopdat.read(ARQ_TESTE)
        n2 = Nwlistopdat.read(ARQ_TESTE)
        assert n1 == n2


def test_neq_nwlistopdat_op2():
    m: MagicMock = mock_open(read_data="".join(MockNwlistopdatOp2))
    with patch("builtins.open", m):
        n1 = Nwlistopdat.read(ARQ_TESTE)
        n2 = Nwlistopdat.read(ARQ_TESTE)
        n2.variaveis_impressao_estagios_agregados[0] = 1
        assert n1 != n2


def test_eq_nwlistopdat_op4():
    m: MagicMock = mock_open(read_data="".join(MockNwlistopdatOp4))
    with patch("builtins.open", m):
        n1 = Nwlistopdat.read(ARQ_TESTE)
        n2 = Nwlistopdat.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
