# Rotinas de testes associadas ao arquivo adterm.dat do NEWAVE
from inewave.newave.sistema import Sistema


sis = Sistema.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(sis.custo_deficit) > 0


def test_escrita_e_leitura():
    sis.escreve_arquivo("tests/_saidas")
    sis2 = Sistema.le_arquivo("tests/_saidas")
    assert sis == sis2


def test_eq_sistema():
    sis2 = Sistema.le_arquivo("tests/_arquivos")
    assert sis == sis2


def test_neq_sistema():
    sis2 = Sistema.le_arquivo("tests/_arquivos")
    sis2.custo_deficit.iloc[0, 0] = -1
    assert sis2 != sis
    assert sis2 is not None
