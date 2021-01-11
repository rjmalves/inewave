# Rotinas de testes associadas ao arquivo cmarg00x.out do NWLISTOP
from inewave.nwlistop.cmarg import LeituraCmarg00
from inewave.config import MESES, NUM_ANOS_ESTUDO
import numpy as np


arquivo_teste = "cmarg00test.out"
leitor = LeituraCmarg00("tests/_arquivos")
leitor.le_arquivos()


def test_leitura():
    assert arquivo_teste in leitor.cmargs


def test_extrai_dados_execucao():
    cmarg = leitor.cmargs[arquivo_teste]
    assert cmarg.mes_pmo == 5
    assert cmarg.ano_pmo == 1995
    assert cmarg.submercado == "SE"


def test_anos_estudo():
    cmarg = leitor.cmargs[arquivo_teste]
    anos_estudo_teste = [1995, 1996, 1997, 1998, 1999]
    anos_lidos = list(cmarg.custos_patamares.keys())
    assert anos_estudo_teste == anos_lidos


def test_cmarg_por_patamar():
    cmarg = leitor.cmargs[arquivo_teste]
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
    for a in [ano + i for i in range(1, NUM_ANOS_ESTUDO)]:
        for m in range(mes, len(MESES) + 1):
            assert np.mean(por_patamar[1][a][m]) > 0.0
