# Rotinas de testes associadas ao arquivo cmarg00x.out do NWLISTOP
from inewave.newave.patamar import LeituraPatamar
import numpy as np  # type: ignore


anos_estudo_teste = [1995, 1996, 1997, 1998, 1999]
leitor = LeituraPatamar("tests/_arquivos")
leitor.le_arquivo()


def test_leitura():
    assert leitor.patamar.num_patamares != 0


def test_anos_estudo():
    assert anos_estudo_teste == leitor.patamar.anos_estudo


def test_leitura_tabela():
    assert np.all(leitor.patamar.patamares >= 0.0)
