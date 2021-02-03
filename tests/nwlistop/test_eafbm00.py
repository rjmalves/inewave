# Rotinas de testes associadas ao arquivo eafbm00x.out do NWLISTOP
from inewave.nwlistop.eafbm00 import LeituraEafbm00
from inewave.config import MESES, NUM_CENARIOS
import numpy as np  # type: ignore


sub_teste = "SUDESTE"
leitor = LeituraEafbm00("tests/_arquivos")
leitor.le_arquivos()
anos_estudo_teste = [1995, 1996, 1997, 1998, 1999]


def test_leitura():
    assert sub_teste in leitor.eafbms


def test_eq_eafbm00():
    leitor2 = LeituraEafbm00("tests/_arquivos")
    leitor2.le_arquivos()
    assert leitor.eafbms == leitor2.eafbms


def test_extrai_dados_execucao():
    eafbm = leitor.eafbms[sub_teste]
    assert eafbm.mes_pmo == 1
    assert eafbm.ano_pmo == 1995
    assert eafbm.submercado == sub_teste


def test_anos_estudo():
    eafbm = leitor.eafbms[sub_teste]
    anos_lidos = list(eafbm.energias_afluentes.keys())
    assert anos_estudo_teste == anos_lidos


def test_eafbm_por_ano():
    eafbm = leitor.eafbms[sub_teste]
    por_ano = eafbm.energias_por_ano
    assert anos_estudo_teste == list(por_ano.keys())
    # Confere se os valores de energia afluente são sempre não nulos
    for a in anos_estudo_teste:
        assert np.all(por_ano[a] > 0.0)


def test_eafbm_por_ano_e_mes():
    eafbm = leitor.eafbms[sub_teste]
    por_ano_e_mes = eafbm.energias_por_ano_e_mes
    assert anos_estudo_teste == list(por_ano_e_mes.keys())
    # Confere se os valores de energia afluente são sempre não nulos
    for a in anos_estudo_teste:
        for m in range(1, len(MESES) + 1):
            assert np.all(por_ano_e_mes[a][m] > 0.0)


def test_eafbm_por_cenario():
    eafbm = leitor.eafbms[sub_teste]
    por_ano_cenario = eafbm.energias_por_ano_e_cenario
    # Confere se os valores de energia afluente são sempre não nulos
    n_meses = len(MESES)
    for a in anos_estudo_teste:
        for c in range(NUM_CENARIOS):
            assert por_ano_cenario[a][c].shape == (n_meses,)
            assert np.all(por_ano_cenario[a][c] > 0)
