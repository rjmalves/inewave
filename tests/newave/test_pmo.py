# Rotinas de testes associadas ao arquivo pmo.dat do NEWAVE
from inewave.newave.pmo import LeituraPMO
from inewave.config import SUBMERCADOS
import numpy as np  # type: ignore


anos_estudo_teste = [1995, 1996, 1997, 1998, 1999]
leitor = LeituraPMO("tests/_arquivos")
leitor.le_arquivo()


def test_leitura_dados_pmo():
    assert leitor.pmo.ano_pmo == 1995
    assert leitor.pmo.mes_pmo == 5
    assert leitor.pmo.versao_newave == "27.4"


def test_anos_estudo():
    assert anos_estudo_teste == leitor.pmo.risco_ens.anos_estudo


def test_leitura_convergencia():
    convergencia = leitor.pmo.convergencia
    tempos = convergencia.tempos_execucao
    zinfs = convergencia.zinf
    zsups = convergencia.zsup
    assert len(tempos) == 45
    assert len(zinfs.keys())
    assert len(zsups.keys())


def test_leitura_ens():
    risco_ens = leitor.pmo.risco_ens
    por_subs_e_ano = risco_ens.ens_por_subsistema_e_ano
    ano = risco_ens.anos_estudo[-1]
    assert list(por_subs_e_ano.keys()) == SUBMERCADOS
    assert por_subs_e_ano["SUDESTE"][ano] == 0.4
    assert por_subs_e_ano["SUL"][ano] == 0.3


def test_leitura_risco():
    risco_ens = leitor.pmo.risco_ens
    por_subs_e_ano = risco_ens.riscos_por_subsistema_e_ano
    ano = risco_ens.anos_estudo[-1]
    assert list(por_subs_e_ano.keys()) == SUBMERCADOS
    assert por_subs_e_ano["SUDESTE"][ano] == 0.05
    assert por_subs_e_ano["SUL"][ano] == 0.05
    assert por_subs_e_ano["NORTE"][ano] == 0.05


def test_leitura_tabelas_custos():
    custo_series = leitor.pmo.custo_series_simuladas
    valor_esp = leitor.pmo.valor_esperado_periodo
    custo_ref = leitor.pmo.custo_referenciado
    assert np.all(custo_series.custos == valor_esp.custos)
    assert np.all(custo_series.custos == custo_ref.custos)
    assert np.all(custo_ref.custos == valor_esp.custos)


def test_eq_pmo():
    leitor2 = LeituraPMO("tests/_arquivos")
    leitor2.le_arquivo()
    assert leitor.pmo == leitor2.pmo
