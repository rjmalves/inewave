# Rotinas de testes associadas ao arquivo dger.dat do NEWAVE
from inewave.newave.dger import DGer


dger = DGer.le_arquivo("tests/_arquivos")


def test_leitura():
    assert len(dger.nome_caso) > 0


def test_nome_caso():
    nome = ("PMO MAIO - 1995  23/04/1995 14:42:20" +
            "  Niveis para 25/04 NW Versao 27")
    assert dger.nome_caso == nome


def test_tipo_execucao():
    assert dger.tipo_execucao == 1


def test_duracao_periodo():
    assert dger.duracao_periodo == 1


def test_num_anos_estudo():
    assert dger.num_anos_estudo == 5


def test_mes_inicio_pre():
    assert dger.mes_inicio_pre_estudo == 1


def test_mes_inicio_estudo():
    assert dger.mes_inicio_estudo == 5


def test_ano_inicio_estudo():
    assert dger.ano_inicio_estudo == 1995


def test_num_anos_pre():
    assert dger.num_anos_pre_estudo == 0


def test_num_anos_pos():
    assert dger.num_anos_pos_estudo == 5


def test_num_anos_pos_final():
    assert dger.num_anos_pos_sim_final == 0


def test_imprime_dados():
    assert dger.imprime_dados == 1


def test_imprime_mercados():
    assert dger.imprime_mercados == 1


def test_imprime_energias():
    assert dger.imprime_energias == 1


def test_imprime_modelo_estocastico():
    assert dger.imprime_modelo_estocastico == 1


def test_imprime_subsistema():
    assert dger.imprime_subsistema == 1


def test_num_max_iteracoes():
    assert dger.num_max_iteracoes == 45


def test_num_forwards():
    assert dger.num_forwards == 200


def test_num_aberturas():
    assert dger.num_aberturas == 20


def test_num_series_sinteticas():
    assert dger.num_series_sinteticas == 2000


def test_ordem_maxima_parp():
    assert dger.ordem_maxima_parp == 6


def test_ano_inicial_historico():
    assert dger.ano_inicial_historico == [1931, 0]


def test_calcula_volume_inicial():
    assert dger.calcula_volume_inicial == 1


def test_volume_inicial_por_subsistema():
    assert dger.volume_inicial_por_subsistema == [0.0, 0.0, 0.0, 0.0, 0.0]


def test_tolerancia():
    assert dger.tolerancia == 95.0


def test_taxa_de_desconto():
    assert dger.taxa_de_desconto == 12.0


def test_tipo_simulacao_final():
    assert dger.tipo_simulacao_final == 1


def test_impressao_operacao():
    assert dger.impressao_operacao == 1


def test_impressao_convergencia():
    assert dger.impressao_convergencia == 1


def test_intervalo_para_gravar():
    assert dger.intervalo_para_gravar == 1


def test_num_minimo_iteracoes():
    assert dger.num_minimo_iteracoes == 30


def test_racionamento_preventivo():
    assert dger.racionamento_preventivo == 1


def test_num_anos_manutencao_utes():
    assert dger.num_anos_manutencao_utes == 1


def test_tendencia_hidrologica():
    assert dger.tendencia_hidrologica == [2, 2]


def test_restricao_itaipu():
    assert dger.restricao_itaipu == 0


def test_bid():
    assert dger.bid == 0


def test_perdas_rede_transmissao():
    assert dger.perdas_rede_transmissao == 0


def test_el_nino():
    assert dger.el_nino == 0


def test_enso():
    assert dger.enso == 0


def test_duracao_por_patamar():
    assert dger.duracao_por_patamar == 1


def test_outros_usos_da_agua():
    assert dger.outros_usos_da_agua == 1


def test_correcao_desvio():
    assert dger.correcao_desvio == 1


def test_curva_aversao():
    assert dger.curva_aversao == 1


def test_tipo_geracao_enas():
    assert dger.tipo_geracao_enas == 0


def test_risco_deficit():
    assert dger.risco_deficit == [1.0, 2.5]


def test_iteracao_para_simulacao_final():
    assert dger.iteracao_para_simulacao_final == 0


def test_agrupamento_livre():
    assert dger.agrupamento_livre == 1


def test_equalizacao_penal_itercambio():
    assert dger.equalizacao_penal_itercambio == 1


def test_representacao_submotorizacao():
    assert dger.representacao_submotorizacao == 2


def test_ordenacao_automatica():
    assert dger.ordenacao_automatica == 0


def test_considera_carga_adicional():
    assert dger.considera_carga_adicional == 1


def test_delta_zsup():
    assert dger.delta_zsup == 10


def test_delta_zinf():
    assert dger.delta_zinf == 0.2


def test_deltas_consecutivos():
    assert dger.deltas_consecutivos == 3


def test_despacho_antecipado_gnl():
    assert dger.despacho_antecipado_gnl == 1


def test_modif_automatica_adterm():
    assert dger.modif_automatica_adterm == 1


def test_considera_ghmin():
    assert dger.considera_ghmin == 1


def test_simulacao_final_com_data():
    assert dger.simulacao_final_com_data == 0


def test_gerenciamento_pls():
    assert dger.gerenciamento_pls == [0, 0, 0, 0, 0]


def test_sar():
    assert dger.sar == 0


def test_cvar():
    assert dger.cvar == 1


def test_considera_zsup_min_convergencia():
    assert dger.considera_zsup_min_convergencia == 0


def test_desconsidera_vazao_minima():
    assert dger.desconsidera_vazao_minima == 0


def test_restricoes_eletricas():
    assert dger.restricoes_eletricas == 1


def test_selecao_de_cortes():
    assert dger.selecao_de_cortes == 1


def test_janela_de_cortes():
    assert dger.janela_de_cortes == 0


def test_reamostragem():
    assert dger.reamostragem_cenarios == [1, 1, 1]


def test_converge_no_zero():
    assert dger.converge_no_zero == 0


def test_consulta_fcf():
    assert dger.consulta_fcf == 0


def test_impressao_ena():
    assert dger.impressao_ena == 0


def test_impressao_cortes_ativos_sim_final():
    assert dger.impressao_cortes_ativos_sim_final == 0


def test_representacao_agregacao():
    assert dger.representacao_agregacao == 1


def test_matriz_correlacao_espacial():
    assert dger.matriz_correlacao_espacial == 1


def test_desconsidera_convergencia_estatistica():
    assert dger.desconsidera_convergencia_estatistica == 1


def test_momento_reamostragem():
    assert dger.momento_reamostragem == 1


def test_mantem_arquivos_energias():
    assert dger.mantem_arquivos_energias == 0


def test_inicio_teste_convergencia():
    assert dger.inicio_teste_convergencia == 1


def test_sazonaliza_vmint():
    assert dger.sazonaliza_vmint == 0


def test_sazonaliza_vmaxt():
    assert dger.sazonaliza_vmaxt == 0


def test_sazonaliza_vminp():
    assert dger.sazonaliza_vminp == 0


def test_sazonaliza_cfuga_cmont():
    assert dger.sazonaliza_cfuga_cmont == 0


def test_restricoes_emissao_gee():
    assert dger.restricoes_emissao_gee == 0


def test_afluencia_anual_parp():
    assert dger.afluencia_anual_parp == [1, 0]


def test_restricoes_fornecimento_gas():
    assert dger.restricoes_fornecimento_gas == 0


def test_incerteza_geracao_eolica():
    assert dger.incerteza_geracao_eolica == 0


def test_incerteza_geracao_solar():
    assert dger.incerteza_geracao_solar == 0


def test_representacao_incertezas():
    assert dger.representacao_incertezas == 0


def test_escrita_e_leitura():
    dger.escreve_arquivo("tests/_saidas")
    dger2 = DGer.le_arquivo("tests/_saidas")
    assert dger == dger2


def test_eq_dger():
    dger2 = DGer.le_arquivo("tests/_arquivos")
    assert dger == dger2


def test_neq_dger():
    dger2 = DGer.le_arquivo("tests/_arquivos")
    dger2.delta_zsup = -10.0
    assert dger != dger2
