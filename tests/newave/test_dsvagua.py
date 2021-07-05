# Rotinas de testes associadas ao arquivo dsvagua.dat do NEWAVE
from inewave.newave.dsvagua import DSVAgua


dsv = DSVAgua.le_arquivo("tests/_arquivos")


def test_leitura():
    assert dsv.desvios.shape[0] > 0


def test_escrita_e_leitura():
    dsv.escreve_arquivo("tests/_saidas")
    dsv2 = DSVAgua.le_arquivo("tests/_saidas")
    assert dsv == dsv2


def test_eq_dsvagua():
    dsv2 = DSVAgua.le_arquivo("tests/_arquivos")
    assert dsv == dsv2


# def test_neq_dsvagua():
#     dsv2 = DSVAgua.le_arquivo("tests/_arquivos")
#     dsv2.le_arquivo()
#     dsv2.dsvagua.tabela[0, 0] = 1e-6
#     assert dsv2.dsvagua != leitor.dsvagua
#     assert dsv2.dsvagua is not None
