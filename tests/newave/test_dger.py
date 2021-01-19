# Rotinas de testes associadas ao arquivo dger.dat do NEWAVE
from inewave.newave.dger import LeituraDGer


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
