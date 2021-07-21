# Rotinas de testes associadas ao arquivo confhd.dat do NEWAVE
from inewave.newave.confhd import Confhd


conf = Confhd.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(conf.usinas) > 0


def test_escrita_e_leitura():
    conf.escreve_arquivo("tests/_saidas")
    conf2 = Confhd.le_arquivo("tests/_saidas")
    assert conf == conf2


def test_eq_confhd():
    conf2 = Confhd.le_arquivo("tests/_arquivos")
    assert conf == conf2


def test_neq_confhd():
    conf2 = Confhd.le_arquivo("tests/_arquivos")
    conf2.usinas.iloc[0, 0] = -1
    assert conf2 != conf
    assert conf2 is not None
