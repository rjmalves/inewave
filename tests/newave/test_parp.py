# Rotinas de testes associadas ao arquivo parp.dat do NEWAVE
from inewave.newave.parp import LeituraPARp
from inewave.config import MESES, ORDEM_MAX_PARP
import numpy as np  # type: ignore

leitor = LeituraPARp("tests/_arquivos")
leitor.le_arquivo()

n_meses = len(MESES)


def test_leitura():
    assert leitor.parp.series_energia[1].shape == (2018 - 1931 + 1,
                                                   n_meses + 1,
                                                   50)
    assert leitor.parp.ordens_orig[1].shape == (5, n_meses + 1)
    assert leitor.parp.coeficientes[1].shape == (5 * n_meses,
                                                 ORDEM_MAX_PARP,
                                                 4)


def test_eq_parp():
    leitor2 = LeituraPARp("tests/_arquivos")
    leitor2.le_arquivo()
    assert leitor.parp == leitor2.parp


def test_neq_parp():
    leitor2 = LeituraPARp("tests/_arquivos")
    leitor2.le_arquivo()
    leitor2.parp.ordens_orig[1] = np.array([])
    assert leitor2.parp != leitor.parp
    assert leitor2.parp is not None


def test_series_energia_ree():
    series = leitor.parp.series_energia_ree(1)
    assert len(series.keys()) == 50


def test_series_medias_ree():
    series = leitor.parp.series_medias_ree(1)
    assert len(series.keys()) == 5


def test_correlograma_energia_ree():
    correl = leitor.parp.correlograma_energia_ree(1)
    assert len(correl.keys()) == 5 * n_meses


def test_correlograma_media_ree():
    correl = leitor.parp.correlograma_media_ree(1)
    assert len(correl.keys()) == 5 * n_meses


def test_ordens_originais_ree():
    ordens = leitor.parp.ordens_originais_ree(1)
    assert len(ordens.keys()) == 5


def test_ordens_finais_ree():
    ordens = leitor.parp.ordens_finais_ree(1)
    assert len(ordens.keys()) == 5


def test_coeficientes_ree():
    coefs = leitor.parp.coeficientes_ree(1)
    assert len(coefs) == 5 * n_meses


def test_correlacoes_espaciais_ano_configuracao():
    corrs = leitor.parp.correlacoes_espaciais_anuais
    assert len(corrs.keys()) == 3


def test_correlacoes_espaciais_mes_configuracao():
    corrs = leitor.parp.correlacoes_espaciais_mensais
    assert len(corrs.keys()) == 3
