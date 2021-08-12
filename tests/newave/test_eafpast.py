# Rotinas de testes associadas ao arquivo eafpast.dat do NEWAVE
from inewave.newave.eafpast import EafPast


eaf = EafPast.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(eaf.tendencia) > 0


def test_escrita_e_leitura():
    eaf.escreve_arquivo("tests/_saidas")
    eaf2 = EafPast.le_arquivo("tests/_saidas")
    assert eaf == eaf2


def test_neq_vazpast():
    eaf2 = EafPast.le_arquivo("tests/_arquivos")
    eaf2.tendencia.iloc[0, 0] = -1
    assert eaf != eaf2
