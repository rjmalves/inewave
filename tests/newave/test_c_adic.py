# Rotinas de testes associadas ao arquivo adterm.dat do NEWAVE
from inewave.newave.cadic import CAdic


cad = CAdic.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(cad.cargas_adicionais) > 0


def test_escrita_e_leitura():
    cad.escreve_arquivo("tests/_saidas")
    cad2 = CAdic.le_arquivo("tests/_saidas")
    assert cad == cad2


def test_eq_cadic():
    cad2 = CAdic.le_arquivo("tests/_arquivos")
    assert cad == cad2


def test_neq_cadic():
    cad2 = CAdic.le_arquivo("tests/_arquivos")
    cad2.cargas_adicionais.iloc[0, 0] = -1
    assert cad2 != cad
    assert cad2 is not None
