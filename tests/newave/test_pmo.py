# Rotinas de testes associadas ao arquivo pmo.dat do NEWAVE
from inewave.newave.pmo import PMO
from inewave.config import REES
import numpy as np  # type: ignore


anos_estudo_teste = [1995, 1996, 1997, 1998, 1999]
pmo = PMO.le_arquivo("tests/_arquivos")


def test_eq_pmo():
    pmo2 = PMO.le_arquivo("tests/_arquivos")
    assert pmo == pmo2


def test_neq_pmo():
    pmo2 = PMO.le_arquivo("tests/_arquivos")
    entrada = pmo2.configuracoes_qualquer_modificacao
    pmo2.configuracoes_alteracao_potencia = entrada
    assert pmo != pmo2


def test_leitura_configs():
    configs = pmo.configuracoes_alteracao_potencia
    assert configs.shape[0] == 10
    for ano in range(configs.shape[0]):
        assert np.all(configs[ano, :] > 0)


def test_leitura_retas_perdas():
    perdas = pmo.retas_perdas_engolimento
    assert len(perdas.keys()) == len(REES)


# def test_leitura_convergencia():
#     convergencia = leitor.pmo.convergencia
#     tempos = convergencia.tempos_execucao
#     zinfs = convergencia.zinf
#     zsups = convergencia.zsup
#     assert len(tempos) == 45
#     assert len(zinfs.keys())
#     assert len(zsups.keys())


# def test_leitura_ens():
#     risco_ens = leitor.pmo.risco_ens
#     por_subs_e_ano = risco_ens.ens_por_subsistema_e_ano
#     ano = risco_ens.anos_estudo[-1]
#     assert list(por_subs_e_ano.keys()) == SUBMERCADOS
#     assert por_subs_e_ano["SUDESTE"][ano] == 0.4
#     assert por_subs_e_ano["SUL"][ano] == 0.3


# def test_leitura_risco():
#     risco_ens = leitor.pmo.risco_ens
#     por_subs_e_ano = risco_ens.riscos_por_subsistema_e_ano
#     ano = risco_ens.anos_estudo[-1]
#     assert list(por_subs_e_ano.keys()) == SUBMERCADOS
#     assert por_subs_e_ano["SUDESTE"][ano] == 0.05
#     assert por_subs_e_ano["SUL"][ano] == 0.05
#     assert por_subs_e_ano["NORTE"][ano] == 0.05


# def test_leitura_tabelas_custos():
#     custo_series = leitor.pmo.custo_series_simuladas
#     valor_esp = leitor.pmo.valor_esperado_periodo
#     custo_ref = leitor.pmo.custo_referenciado
#     assert np.all(custo_series.custos == valor_esp.custos)
#     assert np.all(custo_series.custos == custo_ref.custos)
#     assert np.all(custo_ref.custos == valor_esp.custos)


# # def test_eco_dger_pmo():
# #     leitor2 = LeituraDGer("tests/_arquivos")
# #     leitor2.le_arquivo()
# #     leitor.pmo.dados_gerais.eq_eco_saida(leitor2.dger)


# def test_tabelas_configs():
#     configs_res = leitor.pmo.configuracoes_entrada_reservatorio
#     configs_alt = leitor.pmo.configuracoes_alteracao_potencia
#     configs_exp = leitor.pmo.configuracoes_expansao
#     assert len(list(configs_res.configs_por_ano.keys())) == 10
#     assert len(list(configs_alt.configs_por_ano.keys())) == 10
#     assert len(list(configs_exp.configs_por_ano.keys())) == 10
