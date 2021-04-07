# Rotinas de testes associadas ao arquivo parp.dat do NEWAVE
from typing import Callable, List, Dict

import numpy as np  # type: ignore
from inewave.config import MESES, REES
from inewave.newave.parp import LeituraPARp
from inewave.newave.modelos.parp import PARp
from tests.newave import DIR_TESTES

ARQ_PARP = "parp_parp.dat"
ARQ_PARPA = "parp_parpa.dat"
ARQ_PARPA_SEM_REDORDEM = "parp_parpa_sem_redordem.dat"


# Classe para realizar testes com o parp.dat
class TestesPARp:

    @staticmethod
    def _dimensoes_dict(func: Callable[[int],
                                       Dict[int, np.ndarray]],
                        num_chaves: int,
                        dim_desejada: tuple) -> bool:
        dims: List[bool] = []
        for i_ree, ree in enumerate(REES):
            # Variáveis auxiliares
            elems = func(i_ree + 1)
            chaves = list(elems.keys())
            # Condição do teste
            b = len(chaves) == num_chaves
            for _, serie in elems.items():
                b = serie.shape == dim_desejada
            dims.append(b)
        return all(dims)

    @staticmethod
    def _dimensoes_list(func: Callable[[int],
                                       List[np.ndarray]],
                        num_elementos_desejados: int) -> bool:
        dims: List[bool] = []
        for i_ree, ree in enumerate(REES):
            # Variáveis auxiliares
            elems = func(i_ree + 1)
            # Condição do teste
            b = len(elems) == num_elementos_desejados
            dims.append(b)
        return all(dims)

    @staticmethod
    def confere_dimensoes(parp: PARp,
                          usa_parpa: bool,
                          ano_pmo: int,
                          num_cfgs: int,
                          num_anos_estudo: int) -> bool:

        def _dimensoes_series_energia() -> bool:
            return TestesPARp._dimensoes_dict(parp.series_energia_ree,
                                              num_cfgs,
                                              (ano_pmo - 2 - 1931 + 1,
                                               len(MESES))
                                              )

        def _dimensoes_correl_energia() -> bool:
            return TestesPARp._dimensoes_dict(parp.correlograma_energia_ree,
                                              num_anos_estudo * len(MESES),
                                              (len(MESES) - 1,)
                                              )

        def _dimensoes_ordens_finais() -> bool:
            return TestesPARp._dimensoes_dict(parp.ordens_finais_ree,
                                              num_anos_estudo,
                                              (len(MESES),)
                                              )

        def _dimensoes_ordens_originais() -> bool:
            return TestesPARp._dimensoes_dict(parp.ordens_originais_ree,
                                              num_anos_estudo,
                                              (len(MESES),)
                                              )

        def _dimensoes_coeficientes() -> bool:
            return TestesPARp._dimensoes_list(parp.coeficientes_ree,
                                              num_anos_estudo * len(MESES))

        def _dimensoes_contribuicoes() -> bool:
            return TestesPARp._dimensoes_list(parp.contribuicoes_ree,
                                              num_anos_estudo * len(MESES))

        def _dimensoes_correl_esp_anual() -> bool:
            dims: List[bool] = []
            elems = parp.correlacoes_espaciais_anuais
            cfgs = list(elems.keys())
            b = len(cfgs) == num_cfgs
            for cfg in cfgs:
                chaves_rees = list(elems[cfg].keys())
                b = b and len(chaves_rees) == len(REES)
                for ree in chaves_rees:
                    chaves_internas_rees = list(elems[cfg][ree].keys())
                    b = b and len(chaves_internas_rees) == len(REES)
                dims.append(b)
            return all(dims)

        def _dimensoes_correl_esp_mensal() -> bool:
            dims: List[bool] = []
            elems = parp.correlacoes_espaciais_mensais
            cfgs = list(elems.keys())
            b = len(cfgs) == num_cfgs
            for cfg in cfgs:
                chaves_rees = list(elems[cfg].keys())
                b = b and len(chaves_rees) == len(REES)
                for ree in chaves_rees:
                    chaves_internas_rees = list(elems[cfg][ree].keys())
                    b = b and len(chaves_internas_rees) == len(REES)
                    for ree_interna in chaves_internas_rees:
                        correls = elems[cfg][ree][ree_interna]
                        b = b and correls.shape == (len(MESES), )
                dims.append(b)
            return all(dims)

        return all([_dimensoes_series_energia(),
                    _dimensoes_correl_energia(),
                    _dimensoes_ordens_finais(),
                    _dimensoes_ordens_originais(),
                    _dimensoes_coeficientes(),
                    _dimensoes_contribuicoes(),
                    _dimensoes_correl_esp_anual(),
                    _dimensoes_correl_esp_mensal()])

    @staticmethod
    def confere_dimensoes_medias(parp: PARp,
                                 ano_pmo: int,
                                 num_anos_estudo: int):

        def _dimensoes_series_medias() -> bool:
            return TestesPARp._dimensoes_dict(parp.series_medias_ree,
                                              num_anos_estudo,
                                              (ano_pmo - 2 - 1931 + 1,
                                               len(MESES))
                                              )

        def _dimensoes_correl_medias() -> bool:
            return TestesPARp._dimensoes_dict(parp.correlograma_media_ree,
                                              num_anos_estudo * len(MESES),
                                              (len(MESES),)
                                              )

        return all([_dimensoes_series_medias(),
                    _dimensoes_correl_medias()])


# Testes com o parp.dat de um PMO sem PAR(p)-A
parp_parp = LeituraPARp(DIR_TESTES).le_arquivo(ARQ_PARP)


def test_dimensoes_parp_parp():
    assert TestesPARp.confere_dimensoes(parp_parp,
                                        False,
                                        2020,
                                        60,
                                        10)


def test_dimensoes_medias_parp_parp():
    assert not TestesPARp.confere_dimensoes_medias(parp_parp,
                                                   2020,
                                                   10)


# Testes com o parp.dat de um PMO com PAR(p)-A
parp_parpa = LeituraPARp(DIR_TESTES).le_arquivo(ARQ_PARPA)


def test_dimensoes_parp_parpa():
    assert TestesPARp.confere_dimensoes(parp_parpa,
                                        True,
                                        2020,
                                        50,
                                        10)


def test_dimensoes_medias_parp_parpa():
    assert TestesPARp.confere_dimensoes_medias(parp_parpa,
                                               2020,
                                               10)


# Testes com o parp.dat de um PMO com PAR(p)-A sem Red. Ordem
parp_parpa_sem_red = LeituraPARp(DIR_TESTES).le_arquivo(ARQ_PARPA_SEM_REDORDEM)


def test_dimensoes_parp_parpa_sem_redordem():
    assert TestesPARp.confere_dimensoes(parp_parpa_sem_red,
                                        True,
                                        2020,
                                        50,
                                        10)


def test_dimensoes_medias_parp_parpa_sem_redordem():
    assert TestesPARp.confere_dimensoes_medias(parp_parpa_sem_red,
                                               2020,
                                               10)


# def test_eq_parp():
#     leitor2 = LeituraPARp("tests/_arquivos")
#     leitor2.le_arquivo()
#     assert leitor.parp == leitor2.parp


# def test_neq_parp():
#     leitor2 = LeituraPARp("tests/_arquivos")
#     leitor2.le_arquivo()
#     leitor2.parp.ordens_orig[1] = np.array([])
#     assert leitor2.parp != leitor.parp
#     assert leitor2.parp is not None


# def test_series_energia_ree():
#     series = leitor.parp.series_energia_ree(1)
#     assert len(series.keys()) == 50
#     # Confere valores aleatórios para validar
#     assert series[38][0, 0] == 8428.04
#     assert series[44][6, 4] == 4855.95
#     assert series[44][10, 11] == 7472.84


# def test_series_medias_ree():
#     series = leitor.parp.series_medias_ree(1)
#     assert len(series.keys()) == 10
#     assert not any(series[2024][0, :])
#     # Confere valores aleatórios para validar
#     assert series[2020][9, 0] == 5266.78


# def test_correlograma_energia_ree():
#     correl = leitor.parp.correlograma_energia_ree(1)
#     assert len(correl.keys()) == 5 * n_meses
#     # Confere valores aleatórios para validar
#     assert correl[1][0] == 0.18930
#     assert correl[25][5] == -0.02014


# def test_correlograma_media_ree():
#     correl = leitor.parp.correlograma_media_ree(1)
#     assert len(correl.keys()) == 5 * n_meses
#     # Confere valores aleatórios para validar
#     assert correl[1][0] == 0.29324
#     assert correl[60][5] == 0.88305


# def test_ordens_originais_ree():
#     ordens = leitor.parp.ordens_originais_ree(1)
#     assert len(ordens.keys()) == 10
#     # Confere valores aleatórios para validar
#     assert ordens[2020][1] == 2
#     assert ordens[2024][5] == 6


# def test_ordens_finais_ree():
#     ordens = leitor.parp.ordens_finais_ree(1)
#     assert len(ordens.keys()) == 10
#     # Confere valores aleatórios para validar
#     assert ordens[2020][1] == 1
#     assert ordens[2024][5] == 1


# def test_coeficientes_ree():
#     coefs = leitor.parp.coeficientes_ree(1)
#     assert len(coefs) == 10 * n_meses
#     # Confere valores aleatórios para validar
#     assert len(coefs[0]) == 2
#     assert coefs[0][0] == 0.203
#     assert len(coefs[23]) == 5
#     assert coefs[23][-1] == -0.218


# def test_contribuicoes_ree():
#     contribs = leitor.parp.contribuicoes_ree(1)
#     assert len(contribs) == 10 * n_meses
#     # Confere valores aleatórios para validar
#     assert len(contribs[0]) == 2
#     assert contribs[0][0] == 0.261
#     assert len(contribs[23]) == 5
#     assert contribs[23][-1] == -0.475


# def test_correlacoes_espaciais_ano_configuracao():
#     corrs = leitor.parp.correlacoes_espaciais_anuais
#     n_rees = len(REES)
#     assert len(corrs.keys()) == 3
#     assert all([corrs[1][i][i] == 1
#                 for i in range(1, n_rees + 1)])
#     # Confere valores aleatórios para validar
#     corrs[1][1][2] == -0.1809


# def test_correlacoes_espaciais_mes_configuracao():
#     corrs = leitor.parp.correlacoes_espaciais_mensais
#     assert len(corrs.keys()) == 3
#     # Confere valores aleatórios para validar
#     assert corrs[1][1][2][0] == -0.3822
#     assert corrs[1][1][2][11] == -0.4190
