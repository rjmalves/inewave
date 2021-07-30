# Rotinas de testes associadas ao arquivo earmfpm00x.out do NWLISTOP
from inewave.nwlistop.earmfpm00 import EarmfpM00

sub_teste = "SUDESTE"
earm = EarmfpM00.le_arquivo("tests/_arquivos", "earmfpm00test.out")


def test_leitura():
    assert sub_teste in earm.submercado


def test_eq_earmfpm00():
    earm2 = EarmfpM00.le_arquivo("tests/_arquivos", "earmfpm00test.out")
    assert earm == earm2


def test_neq_earmfpm00():
    earm2 = EarmfpM00.le_arquivo("tests/_arquivos", "earmfpm00test.out")
    earm2.energias.iloc[0, 0] = -1
    assert earm != earm2
