# Rotinas de testes associadas ao arquivo cmarg00x.out do NWLISTOP
from inewave.nwlistop.cmarg import LeituraCmarg00
from inewave.nwlistop._modelos.cmarg00 import Cmarg00


arquivo_teste = "cmarg00test.out" 
leitor = LeituraCmarg00("tests/_arquivos")
leitor.le_arquivos()


def test_leitura():
    assert arquivo_teste in leitor.cmargs

def test_extrai_dados_execucao():
    cmarg = leitor.cmargs[arquivo_teste]
    assert cmarg.mes_pmo == 1
    assert cmarg.ano_pmo == 1995
    assert cmarg.submercado == "SE"

def test_anos_estudo():
    cmarg = leitor.cmargs[arquivo_teste]
    anos_estudo_teste = [1995, 1996, 1997, 1998, 1999]
    anos_lidos = list(cmarg.custos_patamares.keys())
    assert anos_estudo_teste == anos_lidos
