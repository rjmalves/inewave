# Rotinas de testes associadas ao arquivo adterm.dat do NEWAVE
from inewave.newave.adterm import AdTerm


adt = AdTerm.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(adt.despachos) > 0


def test_escrita_e_leitura():
    adt.escreve_arquivo("tests/_saidas")
    adt2 = AdTerm.le_arquivo("tests/_saidas")
    assert adt == adt2


def test_eq_adterm():
    adt2 = AdTerm.le_arquivo("tests/_arquivos")
    assert adt == adt2


def test_neq_adterm():
    adt2 = AdTerm.le_arquivo("tests/_arquivos")
    adt2.despachos.iloc[0, 0] = -1
    assert adt2 != adt
    assert adt2 is not None
