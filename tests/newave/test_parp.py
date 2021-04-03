# Rotinas de testes associadas ao arquivo parp.dat do NEWAVE
from inewave.newave.parp import LeituraPARp
from inewave.config import MESES, ORDEM_MAX_PARP, REES
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
    # Confere valores aleatórios para validar
    assert series[38][0, 0] == 8428.04
    assert series[44][6, 4] == 4855.95
    assert series[44][10, 11] == 7472.84


def test_series_medias_ree():
    series = leitor.parp.series_medias_ree(1)
    assert len(series.keys()) == 5
    assert not any(series[2024][0, :])
    # Confere valores aleatórios para validar
    assert series[2020][9, 0] == 5266.78


def test_correlograma_energia_ree():
    correl = leitor.parp.correlograma_energia_ree(1)
    assert len(correl.keys()) == 5 * n_meses
    # Confere valores aleatórios para validar
    assert correl[1][0] == 0.18930
    assert correl[25][5] == -0.02014


def test_correlograma_media_ree():
    correl = leitor.parp.correlograma_media_ree(1)
    assert len(correl.keys()) == 5 * n_meses
    # Confere valores aleatórios para validar
    assert correl[1][0] == 0.29324
    assert correl[60][5] == 0.88305


def test_ordens_originais_ree():
    ordens = leitor.parp.ordens_originais_ree(1)
    assert len(ordens.keys()) == 5
    # Confere valores aleatórios para validar
    assert ordens[2020][1] == 2
    assert ordens[2024][5] == 6


def test_ordens_finais_ree():
    ordens = leitor.parp.ordens_finais_ree(1)
    assert len(ordens.keys()) == 5
    # Confere valores aleatórios para validar
    assert ordens[2020][1] == 1
    assert ordens[2024][5] == 1


def test_coeficientes_ree():
    coefs = leitor.parp.coeficientes_ree(1)
    assert len(coefs) == 5 * n_meses
    # Confere valores aleatórios para validar
    assert len(coefs[0]) == 2
    assert coefs[0][0] == 0.203
    assert len(coefs[23]) == 5
    assert coefs[23][-1] == -0.218


def test_contribuicoes_ree():
    contribs = leitor.parp.contribuicoes_ree(1)
    assert len(contribs) == 5 * n_meses
    # Confere valores aleatórios para validar
    assert len(contribs[0]) == 2
    assert contribs[0][0] == 0.261
    assert len(contribs[23]) == 5
    assert contribs[23][-1] == -0.475


def test_correlacoes_espaciais_ano_configuracao():
    corrs = leitor.parp.correlacoes_espaciais_anuais
    n_rees = len(REES)
    assert len(corrs.keys()) == 3
    assert all([corrs[1][i][i] == 1
                for i in range(1, n_rees + 1)])
    # Confere valores aleatórios para validar
    corrs[1][1][2] == -0.1809


def test_correlacoes_espaciais_mes_configuracao():
    corrs = leitor.parp.correlacoes_espaciais_mensais
    assert len(corrs.keys()) == 3
    # Confere valores aleatórios para validar
    assert corrs[1][1][2][0] == -0.3822
    assert corrs[1][1][2][11] == -0.4190
