# Rotinas de testes associadas ao arquivo pmo.dat do NEWAVE
from inewave.newave.pmo import PMO
from inewave.config import REES
import numpy as np  # type: ignore


pmo = PMO.le_arquivo("tests/_arquivos")


def test_eq_pmo():
    pmo2 = PMO.le_arquivo("tests/_arquivos")
    assert pmo == pmo2


def test_neq_pmo():
    pmo2 = PMO.le_arquivo("tests/_arquivos")
    entrada = pmo2.configuracoes_qualquer_modificacao
    pmo2.configuracoes_alteracao_potencia = entrada
    assert pmo != pmo2


def test_eafpast_tendencia_hidrologica():
    eafs = pmo.eafpast_tendencia_hidrologica
    assert eafs.shape[0] == 12
    assert eafs.shape[1] == 13
    assert eafs.iloc[0, 1] == 7196.96
    assert eafs.iloc[-1, -1] == 544.91


def test_eafpast_cfuga_medio():
    eafs = pmo.eafpast_cfuga_medio
    assert eafs.shape[0] == 12
    assert eafs.shape[1] == 13
    assert eafs.iloc[0, 1] == 7196.96
    assert eafs.iloc[-1, -1] == 544.91


def test_leitura_configs():
    configs = pmo.configuracoes_alteracao_potencia
    assert configs.shape[0] == 10
    for ano in range(configs.shape[0]):
        assert np.all(configs[ano, :] > 0)


def test_leitura_retas_perdas():
    perdas = pmo.retas_perdas_engolimento
    assert len(perdas.keys()) == len(REES)


def test_leitura_convergencia():
    convergencia = pmo.convergencia
    assert len(list(convergencia.index)) == 135


def test_leitura_ens():
    risco_ens = pmo.risco_deficit_ens
    assert len(list(risco_ens.index)) == 5
    assert risco_ens.iloc[4, 1] == 0.05
    assert risco_ens.iloc[4, 2] == 0.4
    assert risco_ens.iloc[4, 3] == 0.05
    assert risco_ens.iloc[4, 4] == 0.3


def test_leitura_tabelas_custos():
    custo_series = pmo.custo_operacao_series_simuladas
    valor_esp = pmo.valor_esperado_periodo_estudo
    custo_ref = pmo.custo_operacao_referenciado_primeiro_mes
    assert custo_series.iloc[0, 0] == 18951.33
    assert valor_esp.iloc[0, 0] == 18951.33
    assert custo_ref.iloc[0, 0] == 18951.33


# def test_eco_dger_pmo():
#     leitor2 = LeituraDGer("tests/_arquivos")
#     leitor2.le_arquivo()
#     leitor.pmo.dados_gerais.eq_eco_saida(leitor2.dger)
