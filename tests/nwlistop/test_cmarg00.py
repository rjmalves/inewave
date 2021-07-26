# Rotinas de testes associadas ao arquivo cmarg00x.out do NWLISTOP
from inewave.nwlistop.cmarg00 import Cmarg00


cmarg = Cmarg00.le_arquivo("tests/_arquivos", "cmarg00test.out")


def test_leitura():
    assert cmarg.submercado == "SUDESTE"
    assert cmarg.custos.shape[0] == 30000


def test_eq_cmarg00():
    cmarg2 = Cmarg00.le_arquivo("tests/_arquivos", "cmarg00test.out")
    assert cmarg == cmarg2


def test_neq_cmarg00():
    cmarg2 = Cmarg00.le_arquivo("tests/_arquivos", "cmarg00test.out")
    cmarg2.custos.iloc[0, 0] = -1
    assert cmarg != cmarg2
