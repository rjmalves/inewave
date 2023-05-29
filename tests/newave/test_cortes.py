from inewave.newave.cortes import Cortes

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch
import pytest
import pandas as pd

ARQ_TESTE_REE = "./tests/mocks/arquivos/cortes_ree.dat"
ARQ_TESTE_HIB = "./tests/mocks/arquivos/cortes_hib.dat"

TAMANHO_CORTE_REE = 1664
REES_CORTE = [1, 6, 7, 5, 10, 12, 2, 11, 3, 4, 8, 9]
UHES_CORTE = list(range(154))
SUBMERCADOS_CORTE = [1, 2, 3, 4]
TAMANHO_CORTE_HIB = 17568


def test_atributos_encontrados_cortes_ree():
    h = Cortes.read(
        ARQ_TESTE_REE,
        tamanho_registro=TAMANHO_CORTE_REE,
        indice_ultimo_corte=1,
        numero_total_cortes=1,
        codigos_rees=REES_CORTE,
        codigos_submercados=SUBMERCADOS_CORTE,
    )
    assert isinstance(h.cortes, pd.DataFrame)


def test_atributos_encontrados_cortes_hib():
    h = Cortes.read(
        ARQ_TESTE_HIB,
        tamanho_registro=TAMANHO_CORTE_HIB,
        indice_ultimo_corte=1,
        numero_total_cortes=1,
        codigos_uhes=UHES_CORTE,
        codigos_submercados=SUBMERCADOS_CORTE,
    )
    assert isinstance(h.cortes, pd.DataFrame)


def test_eq_cortes():
    h1 = Cortes.read(
        ARQ_TESTE_HIB,
        tamanho_registro=TAMANHO_CORTE_HIB,
        indice_ultimo_corte=1,
        numero_total_cortes=1,
        codigos_uhes=UHES_CORTE,
        codigos_submercados=SUBMERCADOS_CORTE,
    )
    h2 = Cortes.read(
        ARQ_TESTE_HIB,
        tamanho_registro=TAMANHO_CORTE_HIB,
        indice_ultimo_corte=1,
        numero_total_cortes=1,
        codigos_uhes=UHES_CORTE,
        codigos_submercados=SUBMERCADOS_CORTE,
    )
    assert h1 == h2


def test_atributos_cortes_ree():
    h = Cortes.read(
        ARQ_TESTE_REE,
        tamanho_registro=TAMANHO_CORTE_REE,
        indice_ultimo_corte=1,
        numero_total_cortes=1,
        codigos_rees=REES_CORTE,
        codigos_submercados=SUBMERCADOS_CORTE,
    )
    assert h.cortes.at[0, "indice_corte"] == 1
    assert h.cortes.at[0, "iteracao_construcao"] == 1
    assert h.cortes.at[0, "indice_forward"] == 1
    assert h.cortes.at[0, "iteracao_desativacao"] == 0
    assert h.cortes.at[0, "rhs"] == 1017842.32745
    assert h.cortes.at[0, "pi_earm_ree1"] == -0.00015
    assert h.cortes.at[0, "pi_earm_ree12"] == -0.00021
    assert h.cortes.at[0, "pi_ena_ree1_lag1"] == 0.00084
    assert h.cortes.at[0, "pi_ena_ree7_lag1"] == -0.00013
    assert h.cortes.at[0, "pi_gnl_sbm1_pat1_lag1"] == -0.00021
    assert h.cortes.at[0, "pi_gnl_sbm2_pat3_lag1"] == -0.00191


def test_atributos_cortes_hib():
    h = Cortes.read(
        ARQ_TESTE_HIB,
        tamanho_registro=TAMANHO_CORTE_HIB,
        indice_ultimo_corte=1,
        numero_total_cortes=1,
        codigos_uhes=UHES_CORTE,
        codigos_submercados=SUBMERCADOS_CORTE,
    )
    assert h.cortes.at[0, "indice_corte"] == 1
    assert h.cortes.at[0, "iteracao_construcao"] == 100
    assert h.cortes.at[0, "indice_forward"] == 200
    assert h.cortes.at[0, "iteracao_desativacao"] == 100
    assert h.cortes.at[0, "rhs"] == 279953222.04742
    assert h.cortes.at[0, "pi_gnl_sbm1_pat1_lag1"] == -1.21847
    assert h.cortes.at[0, "pi_gnl_sbm3_pat3_lag2"] == -2.46932
    assert h.cortes.at[0, "pi_varm_uhe0"] == -6.74723
    assert h.cortes.at[0, "pi_varm_uhe153"] == -0.37228
    assert h.cortes.at[0, "pi_qafl_uhe0_lag12"] == 0.53852
