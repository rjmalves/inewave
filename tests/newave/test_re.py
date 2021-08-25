# Rotinas de testes associadas ao arquivo adterm.dat do NEWAVE
from inewave.newave.re import RE


res = RE.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(res.restricoes) > 0


def test_escrita_e_leitura():
    res.escreve_arquivo("tests/_saidas")
    res2 = RE.le_arquivo("tests/_saidas")
    assert res == res2


def test_eq_re():
    res2 = RE.le_arquivo("tests/_arquivos")
    assert res == res2


def test_neq_re():
    res2 = RE.le_arquivo("tests/_arquivos")
    res2.restricoes.iloc[0, 0] = -1
    assert res2 != res
    assert res2 is not None
