# Rotinas de testes associadas ao arquivo eafbm00x.out do NWLISTOP
from inewave.nwlistop.eafbm00 import EafbM00


sub_teste = "SUDESTE"
eaf = EafbM00.le_arquivo("tests/_arquivos", "eafbm00test.out")


def test_leitura():
    assert sub_teste == eaf.submercado


def test_eq_eafbm00():
    eaf2 = EafbM00.le_arquivo("tests/_arquivos", "eafbm00test.out")
    assert eaf == eaf2


def test_neq_eafbm00():
    eaf2 = EafbM00.le_arquivo("tests/_arquivos", "eafbm00test.out")
    eaf2.energias.iloc[0, 0] = -1
    assert eaf != eaf2
