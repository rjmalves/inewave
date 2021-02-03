# Rotinas de testes associadas ao arquivo earmfpm00x.out do NWLISTOP
from inewave.nwlistop.earmfpm00 import LeituraEarmfpm00
from inewave.config import MESES, NUM_CENARIOS
import numpy as np  # type: ignore


sub_teste = "SUDESTE"
leitor = LeituraEarmfpm00("tests/_arquivos")
leitor.le_arquivos()
anos_estudo_teste = [1995, 1996, 1997, 1998, 1999]


def test_leitura():
    assert sub_teste in leitor.earmfpms


def test_eq_earmfpm00():
    leitor2 = LeituraEarmfpm00("tests/_arquivos")
    leitor2.le_arquivos()
    assert leitor.earmfpms == leitor2.earmfpms


def test_extrai_dados_execucao():
    earmfpm = leitor.earmfpms[sub_teste]
    assert earmfpm.mes_pmo == 5
    assert earmfpm.ano_pmo == 1995
    assert earmfpm.submercado == sub_teste


def test_anos_estudo():
    earmfpm = leitor.earmfpms[sub_teste]
    anos_lidos = list(earmfpm.energias_armazenadas.keys())
    assert anos_estudo_teste == anos_lidos


def test_earmfpm_por_ano():
    earmfpm = leitor.earmfpms[sub_teste]
    por_ano = earmfpm.energias_por_ano
    assert anos_estudo_teste == list(por_ano.keys())
    mes = earmfpm.mes_pmo
    ano = earmfpm.ano_pmo
    # Confere se os valores médios de energias nos meses anteriores
    # ao estudo são nulos, e todos os posteriores são > 0
    assert np.all(por_ano[ano][:, :mes-1] == 0.0)
    assert np.all(por_ano[ano][:, mes-1:] > 0.0)
    for a in list(por_ano.keys())[1:]:
        assert np.all(por_ano[a] > 0.0)


def test_earmfpm_por_ano_e_mes():
    earmfpm = leitor.earmfpms[sub_teste]
    por_ano_e_mes = earmfpm.energias_por_ano_e_mes
    assert anos_estudo_teste == list(por_ano_e_mes.keys())
    mes = earmfpm.mes_pmo
    ano = earmfpm.ano_pmo
    # Confere se os valores médios de energias nos meses anteriores
    # ao estudo são nulos, e todos os posteriores são > 0
    for m in range(1, mes):
        assert np.all(por_ano_e_mes[ano][m] == 0.0)
    for m in range(mes, len(MESES) + 1):
        assert np.all(por_ano_e_mes[ano][m] > 0.0)
    for a in list(por_ano_e_mes.keys())[1:]:
        for m in range(mes, len(MESES) + 1):
            assert np.all(por_ano_e_mes[a][m] > 0.0)


def test_earmfpm_por_cenario():
    earmfpm = leitor.earmfpms[sub_teste]
    por_ano_cenario = earmfpm.energias_por_ano_e_cenario
    mes_pmo = earmfpm.mes_pmo
    # Confere se os valores lidos são nulos até o mês anterior
    # ao PMO, e positivos do mês do PMO em diante.
    anos = anos_estudo_teste
    n_meses = len(MESES)
    for c in range(NUM_CENARIOS):
        assert por_ano_cenario[anos[0]][c].shape == (n_meses,)
        assert np.all(por_ano_cenario[anos[0]][c][:mes_pmo-1] == 0)
        assert np.all(por_ano_cenario[anos[0]][c][mes_pmo-1:] > 0)
    for a in anos[1:]:
        for c in range(NUM_CENARIOS):
            assert por_ano_cenario[a][c].shape == (n_meses,)
            assert np.all(por_ano_cenario[a][c] > 0)
