# Rotinas de testes associadas ao arquivo parp.dat do NEWAVE
from inewave.newave.parp import LeituraPARp
from inewave.config import MESES, ORDEM_MAX_PARP

leitor = LeituraPARp("tests/_arquivos")
leitor.le_arquivo()

n_meses = len(MESES)


def test_leitura():
    assert leitor.parp.series[1].shape == (2018 - 1931 + 1,
                                           n_meses + 1,
                                           56)
    assert leitor.parp.ordens[1].shape == (5, n_meses + 1)
    assert leitor.parp.coeficientes[1].shape == (5 * n_meses,
                                                 ORDEM_MAX_PARP,
                                                 2)


def test_eq_parp():
    leitor2 = LeituraPARp("tests/_arquivos")
    leitor2.le_arquivo()
    assert leitor.parp == leitor2.parp
