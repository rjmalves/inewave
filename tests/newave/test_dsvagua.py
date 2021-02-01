# Rotinas de testes associadas ao arquivo dsvagua.dat do NEWAVE
from inewave.newave.dsvagua import LeituraDSVAgua, EscritaDSVAgua


leitor = LeituraDSVAgua("tests/_arquivos")
leitor.le_arquivo()


def test_leitura():
    assert leitor.dsvagua.tabela.shape[0] > 0


def test_escrita_e_leitura():
    escritor = EscritaDSVAgua("tests/_saidas")
    escritor.escreve_arquivo(leitor.dsvagua)
    leitor2 = LeituraDSVAgua("tests/_saidas")
    leitor2.le_arquivo()
    assert leitor.dsvagua == leitor2.dsvagua
