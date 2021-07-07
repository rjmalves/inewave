# Rotinas de testes associadas ao arquivo dger.dat do NEWAVE
from inewave.newave.dger import DGer


dger = DGer.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(dger.nome_caso) > 0


def test_ano_inicio_estudo():
    assert dger.ano_inicio_estudo == 1995


def test_tolerancia():
    assert dger.tolerancia == 95.0


def test_risco_deficit():
    assert dger.risco_deficit == [1.0, 2.5]


def test_reamostragem():
    assert dger.reamostragem_cenarios == [1, 1, 1]


def test_escrita_e_leitura():
    dger.escreve_arquivo("tests/_saidas")
    dger2 = DGer.le_arquivo("tests/_saidas")
    assert dger == dger2


def test_eq_dger():
    dger2 = DGer.le_arquivo("tests/_arquivos")
    assert dger == dger2


def test_neq_dger():
    dger2 = DGer.le_arquivo("tests/_arquivos")
    dger2.delta_zsup = -10.0
    assert dger != dger2
