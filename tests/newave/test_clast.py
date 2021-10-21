# Rotinas de testes associadas ao arquivo clast.dat do NEWAVE
from inewave.newave.clast import ClasT

clas = ClasT.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(clas.usinas) > 0


def test_escrita_e_leitura():
    clas.escreve_arquivo("tests/_saidas")
    clas2 = ClasT.le_arquivo("tests/_saidas")
    assert clas == clas2


def test_eq_clast():
    clas2 = ClasT.le_arquivo("tests/_arquivos")
    assert clas == clas2


def test_neq_clast():
    clas2 = ClasT.le_arquivo("tests/_arquivos")
    clas2.usinas.iloc[0, 0] = -1
    assert clas2 != clas
    assert clas2 is not None
