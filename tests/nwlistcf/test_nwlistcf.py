from inewave.nwlistcf.nwlistcf import Nwlistcf

fcf = Nwlistcf.le_arquivo("./tests/_arquivos")


def test_leitura():
    assert len(fcf.registros) > 0


def test_eq_nwlistcf():
    fcf2 = Nwlistcf.le_arquivo("./tests/_arquivos")
    assert fcf2 == fcf


# def test_neq_nwlistcf():
#     leitor2 = LeituraNwlistcf("./tests/_arquivos")
#     leitor2.le_arquivo()
#     leitor2.nwlistcf.registros[5] = {}
#     assert leitor2.nwlistcf != leitor.nwlistcf
