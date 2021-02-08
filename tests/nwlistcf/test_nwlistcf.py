from inewave.nwlistcf.nwlistcf import LeituraNwlistcf

leitor = LeituraNwlistcf("./tests/_arquivos")
leitor.le_arquivo()


def test_leitura():
    assert len(leitor.nwlistcf.registros.keys()) > 0


def test_eq_nwlistcf():
    leitor2 = LeituraNwlistcf("./tests/_arquivos")
    leitor2.le_arquivo()
    assert leitor2.nwlistcf == leitor.nwlistcf


def test_neq_nwlistcf():
    leitor2 = LeituraNwlistcf("./tests/_arquivos")
    leitor2.le_arquivo()
    leitor2.nwlistcf.registros[5] = {}
    assert leitor2.nwlistcf != leitor.nwlistcf
