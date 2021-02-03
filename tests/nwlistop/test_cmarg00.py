# Rotinas de testes associadas ao arquivo cmarg00x.out do NWLISTOP
from inewave.newave.patamar import LeituraPatamar
from inewave.nwlistop.cmarg00 import LeituraCmarg00
from inewave.config import MESES, NUM_CENARIOS
import numpy as np  # type: ignore


sub_teste = "SUDESTE"
leitor = LeituraCmarg00("tests/_arquivos")
leitor.le_arquivos()


def test_leitura():
    assert sub_teste in leitor.cmargs


def test_eq_cmarg00():
    leitor2 = LeituraCmarg00("tests/_arquivos")
    leitor2.le_arquivos()
    assert leitor.cmargs == leitor2.cmargs


def test_extrai_dados_execucao():
    cmarg = leitor.cmargs[sub_teste]
    assert cmarg.mes_pmo == 5
    assert cmarg.ano_pmo == 1995
    assert cmarg.submercado == sub_teste


def test_anos_estudo():
    cmarg = leitor.cmargs[sub_teste]
    anos_estudo_teste = [1995, 1996, 1997, 1998, 1999]
    anos_lidos = list(cmarg.custos_patamares.keys())
    assert anos_estudo_teste == anos_lidos


def test_cmarg_por_patamar():
    cmarg = leitor.cmargs[sub_teste]
    por_patamar = cmarg.custos_por_patamar
    assert [1, 2, 3] == list(por_patamar.keys())
    mes = cmarg.mes_pmo
    ano = cmarg.ano_pmo
    # Confere se os valores médios de custos nos meses anteriores
    # ao estudo são nulos, e todos os posteriores são > 0
    for m in range(1, mes):
        assert np.mean(por_patamar[1][ano][m]) == 0.0
    for m in range(mes, len(MESES) + 1):
        assert np.mean(por_patamar[1][ano][m]) > 0.0
    for a in list(por_patamar[1].keys())[1:]:
        for m in range(mes, len(MESES) + 1):
            assert np.mean(por_patamar[1][a][m]) > 0.0


def test_cmarg_por_ano():
    cmarg = leitor.cmargs[sub_teste]
    por_ano = cmarg.custos_por_ano
    assert [1, 2, 3] == list(por_ano.keys())
    mes = cmarg.mes_pmo
    ano = cmarg.ano_pmo
    # Confere se os valores médios de custos nos meses anteriores
    # ao estudo são nulos, e todos os posteriores são > 0
    assert np.mean(por_ano[1][ano][:, :mes-1]) == 0.0
    assert np.mean(por_ano[1][ano][:, mes-1:]) > 0.0
    for a in list(por_ano[1].keys())[1:]:
        assert np.mean(por_ano[1][a]) > 0.0


def test_cmarg_por_ano_e_mes():
    cmarg = leitor.cmargs[sub_teste]
    por_ano_e_mes = cmarg.custos_por_ano_e_mes
    assert [1, 2, 3] == list(por_ano_e_mes.keys())
    mes = cmarg.mes_pmo
    ano = cmarg.ano_pmo
    # Confere se os valores médios de custos nos meses anteriores
    # ao estudo são nulos, e todos os posteriores são > 0
    for m in range(1, mes):
        assert np.mean(por_ano_e_mes[1][ano][m]) == 0.0
    for m in range(mes, len(MESES) + 1):
        assert np.mean(por_ano_e_mes[1][ano][m]) > 0.0
    for a in list(por_ano_e_mes[1].keys())[1:]:
        for m in range(mes, len(MESES) + 1):
            assert np.mean(por_ano_e_mes[1][a][m]) > 0.0


def test_cmarg_medio_por_ano():
    cmarg = leitor.cmargs[sub_teste]
    le_patamar = LeituraPatamar("tests/_arquivos")
    patamar = le_patamar.le_arquivo()
    medios = cmarg.custos_medios_por_ano(patamar)
    n_meses = len(MESES)
    mes_pmo = cmarg.mes_pmo
    # Confere se os valores médios segundo os patamares
    # são nulos até o mês anterior ao PMO
    anos = patamar.anos_estudo
    assert np.all(medios[anos[0]][:, :mes_pmo-1] == 0)
    for a in anos:
        assert medios[a].shape == (NUM_CENARIOS, n_meses)


def test_cmarg_medio_por_ano_e_mes():
    cmarg = leitor.cmargs[sub_teste]
    le_patamar = LeituraPatamar("tests/_arquivos")
    patamar = le_patamar.le_arquivo()
    medios = cmarg.custos_medios_por_ano_e_mes(patamar)
    n_meses = len(MESES)
    mes_pmo = cmarg.mes_pmo
    # Confere se os valores médios segundo os patamares
    # são nulos até o mês anterior ao PMO
    anos = patamar.anos_estudo
    for m in range(1, mes_pmo):
        assert np.all(medios[anos[0]][m] == 0)
    for a in anos:
        for m in range(1, n_meses + 1):
            custos: np.ndarray = medios[a][m]
            assert custos.shape == (NUM_CENARIOS,)
