# Rotinas de testes associadas ao arquivo term.dat do NEWAVE
from inewave.newave.term import Term


term = Term.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(term.usinas) > 0


def test_escrita_e_leitura():
    term.escreve_arquivo("tests/_saidas")
    term2 = Term.le_arquivo("tests/_saidas")
    assert term == term2


def test_eq_term():
    term2 = Term.le_arquivo("tests/_arquivos")
    assert term == term2


def test_neq_term():
    term2 = Term.le_arquivo("tests/_arquivos")
    term2.usinas.iloc[0, 0] = -1
    assert term2 != term
    assert term2 is not None
