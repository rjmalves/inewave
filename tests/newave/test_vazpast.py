# Rotinas de testes associadas ao arquivo vazpast.dat do NEWAVE
from inewave.newave.vazpast import LeituraVazPast, EscritaVazPast
import numpy as np  # type: ignore


leitor = LeituraVazPast("tests/_arquivos")
leitor.le_arquivo()


def test_leitura():
    assert len(leitor.vazpast.postos) > 0
    assert len(leitor.vazpast.nomes) > 0
    assert leitor.vazpast.tabela.shape[0] > 0


def test_escrita_e_leitura():
    escritor = EscritaVazPast("tests/_saidas")
    escritor.escreve_arquivo(leitor.vazpast)
    leitor2 = LeituraVazPast("tests/_saidas")
    leitor2.le_arquivo()
    assert leitor.vazpast == leitor2.vazpast


def test_eq_vazpast():
    leitor2 = LeituraVazPast("tests/_arquivos")
    leitor2.le_arquivo()
    leitor2.vazpast.tabela = np.array([])
    assert leitor.vazpast != leitor2.vazpast


def test_neq_vazpast():
    leitor2 = LeituraVazPast("tests/_arquivos")
    leitor2.le_arquivo()
    leitor2.vazpast.tabela = np.array([])
    assert leitor.vazpast != leitor2.vazpast
