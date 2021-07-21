# Rotinas de testes associadas ao arquivo vazpast.dat do NEWAVE
from inewave.newave.vazpast import VazPast


vaz = VazPast.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(vaz.tendencia) > 0


def test_escrita_e_leitura():
    vaz.escreve_arquivo("tests/_saidas")
    vaz2 = VazPast.le_arquivo("tests/_saidas")
    assert vaz == vaz2


def test_neq_vazpast():
    vaz2 = VazPast.le_arquivo("tests/_arquivos")
    vaz2.tendencia.iloc[0, 0] = -1
    assert vaz != vaz2
