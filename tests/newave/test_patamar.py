# Rotinas de testes associadas ao arquivo patamar.dat do NEWAVE
from inewave.newave.patamar import LeituraPatamar
from inewave.config import MESES
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


def test_patamar_por_ano():
    patamares_ano = leitor.patamar.patamares_por_ano
    assert anos_estudo_teste == list(patamares_ano.keys())
    # Verifica as dimensões de cada conjunto de patamares
    # e se todos os valores são maiores que 0
    n_meses = len(MESES)
    for ano in anos_estudo_teste:
        p = patamares_ano[ano]
        assert p.shape == (leitor.patamar.num_patamares,
                           n_meses)
        assert np.all(p > 0.0)


def test_patamar_por_ano_e_mes():
    patamares_ano = leitor.patamar.patamares_por_ano_e_mes
    assert anos_estudo_teste == list(patamares_ano.keys())
    # Verifica as dimensões de cada conjunto de patamares
    # e se todos os valores são maiores que 0
    for ano in anos_estudo_teste:
        for mes in range(1, len(MESES) + 1):
            p = patamares_ano[ano][mes]
            assert p.shape == (leitor.patamar.num_patamares,)
            assert np.all(p > 0.0)


def test_eq_patamar():
    leitor2 = LeituraPatamar("tests/_arquivos")
    leitor2.le_arquivo()
    assert leitor.patamar == leitor2.patamar
