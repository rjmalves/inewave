# Rotinas de testes associadas ao arquivo adterm.dat do NEWAVE
from inewave.newave.curva import Curva


cur = Curva.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(cur.curva_seguranca) > 0


def test_escrita_e_leitura():
    cur.escreve_arquivo("tests/_saidas")
    cur2 = Curva.le_arquivo("tests/_saidas")
    assert cur == cur2


def test_eq_curva():
    cur2 = Curva.le_arquivo("tests/_arquivos")
    assert cur == cur2


def test_neq_curva():
    cur2 = Curva.le_arquivo("tests/_arquivos")
    cur2.curva_seguranca.iloc[0, 0] = -1
    assert cur2 != cur
    assert cur2 is not None
