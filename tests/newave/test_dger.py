# Rotinas de testes associadas ao arquivo dger.dat do NEWAVE
from inewave.newave.modelos.dger import DGer
from inewave.newave.dger import LeituraDGer, EscritaDGer


leitor = LeituraDGer("tests/_arquivos")
leitor.le_arquivo()


def test_leitura():
    assert len(leitor.dger.nome_estudo) > 0


def test_ano_inicio_estudo():
    assert leitor.dger.ano_inicio_estudo == 1995


def test_tolerancia():
    assert leitor.dger.tolerancia == 95.0


def test_risco_deficit():
    assert leitor.dger.profundidade_risco_deficit == (1.0, 2.5)


def test_reamostragem():
    assert leitor.dger.reamostragem


def test_dger_padrao():
    dger_padrao = DGer.dger_padrao()
    escritor = EscritaDGer("tests/_saidas")
    escritor.escreve_arquivo(dger_padrao)
    leitor_padrao = LeituraDGer("tests/_saidas")
    leitor_padrao.le_arquivo()
    assert leitor_padrao.dger == dger_padrao


def test_escrita_e_leitura():
    escritor = EscritaDGer("tests/_saidas")
    escritor.escreve_arquivo(leitor.dger)
    leitor2 = LeituraDGer("tests/_saidas")
    leitor2.le_arquivo()
    assert leitor.dger == leitor2.dger
