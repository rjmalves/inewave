# Rotinas de testes associadas ao arquivo patamar.dat do NEWAVE
from inewave.newave.patamar import Patamar
from inewave.config import MESES, NUM_PATAMARES
import numpy as np  # type: ignore


anos_estudo_teste = [1995, 1996, 1997, 1998, 1999]
pat = Patamar.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(pat.anos_estudo) > 0


def test_eq_patamar():
    pat2 = Patamar.le_arquivo("tests/_arquivos")
    assert pat == pat2


def test_neq_patamar():
    pat2 = Patamar.le_arquivo("tests/_arquivos")
    pat2.anos_estudo = [1990, 1991, 1992, 1993, 1994]
    assert pat != pat2


def test_anos_estudo():
    assert anos_estudo_teste == pat.anos_estudo


def test_patamar_por_ano():
    patamares_ano = pat.patamares_por_ano
    assert anos_estudo_teste == list(patamares_ano.keys())
    # Verifica as dimensões de cada conjunto de patamares
    # e se todos os valores são maiores que 0
    for ano in anos_estudo_teste:
        p = patamares_ano[ano]
        assert p.shape == (NUM_PATAMARES,
                           len(MESES))
        assert np.all(p > 0.0)
