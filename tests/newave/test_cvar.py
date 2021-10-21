# Rotinas de testes associadas ao arquivo cvar.dat do NEWAVE
from inewave.newave.cvar import CVAR

cvar = CVAR.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(cvar.valores_constantes) > 0
    assert len(cvar.alfa_variavel) > 0
    assert len(cvar.lambda_variavel) > 0


def test_escrita_e_leitura():
    cvar.escreve_arquivo("tests/_saidas")
    cvar2 = CVAR.le_arquivo("tests/_saidas")
    assert cvar == cvar2


def test_eq_cvar():
    cvar2 = CVAR.le_arquivo("tests/_arquivos")
    assert cvar == cvar2


def test_neq_cvar():
    cvar2 = CVAR.le_arquivo("tests/_arquivos")
    cvar2.valores_constantes = [0, 0]
    assert cvar2 != cvar
    assert cvar2 is not None
