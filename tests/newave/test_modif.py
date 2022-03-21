# Rotinas de testes associadas ao arquivo modif.dat do NEWAVE
from inewave.newave.modif import Modif


modif = Modif.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(modif.modificacoes_usina(1)) > 0


def test_escrita_e_leitura():
    modif.escreve_arquivo("tests/_saidas")
    modif2 = Modif.le_arquivo("tests/_saidas")
    assert modif == modif2


def test_eq_curva():
    modif2 = Modif.le_arquivo("tests/_arquivos")
    assert modif == modif2


def test_neq_curva():
    modif2 = Modif.le_arquivo("tests/_arquivos")
    modif2.usina[0].nome = "Errado"
    assert modif2 != modif
    assert modif2 is not None
