# Rotinas de testes associadas ao arquivo dger.dat do NEWAVE
from inewave.newave.dger import DGer

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.dger import MockDger


def test_atributos_nao_encontrados_dger():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.nome_caso == ""
        assert d.tipo_execucao is None
        assert d.duracao_periodo is None
        assert d.num_anos_estudo is None
        assert d.mes_inicio_pre_estudo is None
        assert d.mes_inicio_estudo is None
        assert d.ano_inicio_estudo is None
        assert d.num_anos_pre_estudo is None
        assert d.num_anos_pos_estudo is None
        assert d.num_anos_pos_sim_final is None
        assert d.imprime_dados is None
        assert d.imprime_mercados is None
        assert d.imprime_energias is None
        assert d.imprime_modelo_estocastico is None
        assert d.imprime_subsistema is None
        assert d.num_max_iteracoes is None
        assert d.num_forwards is None
        assert d.num_aberturas is None
        assert d.num_series_sinteticas is None
        assert d.ordem_maxima_parp is None
        assert d.ano_inicial_historico is None
        assert d.tamanho_registro_arquivo_historico is None
        assert d.calcula_volume_inicial is None
        assert d.volume_inicial_subsistema == [
            None,
            None,
            None,
            None,
            None,
        ]
        assert d.tolerancia is None
        assert d.taxa_de_desconto is None
        assert d.tipo_simulacao_final is None
        assert d.agregacao_simulacao_final is None
        assert d.impressao_operacao is None
        assert d.impressao_convergencia is None
        assert d.intervalo_para_gravar is None
        assert d.num_minimo_iteracoes is None
        assert d.racionamento_preventivo is None
        assert d.num_anos_manutencao_utes is None
        assert d.considera_tendencia_hidrologica_calculo_politica is None
        assert d.considera_tendencia_hidrologica_sim_final is None
        assert d.restricao_itaipu is None
        assert d.bid is None
        assert d.perdas_rede_transmissao is None
        assert d.el_nino is None
        assert d.enso is None
        assert d.duracao_por_patamar is None
        assert d.outros_usos_da_agua is None
        assert d.correcao_desvio is None
        assert d.curva_aversao is None
        assert d.tipo_geracao_enas is None
        assert d.primeira_profundidade_risco_deficit is None
        assert d.segunda_profundidade_risco_deficit is None
        assert d.iteracao_para_simulacao_final is None
        assert d.agrupamento_livre is None
        assert d.equalizacao_penal_intercambio is None
        assert d.representacao_submotorizacao is None
        assert d.ordenacao_automatica is None
        assert d.considera_carga_adicional is None
        assert d.delta_zsup is None
        assert d.delta_zinf is None
        assert d.deltas_consecutivos is None
        assert d.despacho_antecipado_gnl is None
        assert d.modif_automatica_adterm is None
        assert d.considera_ghmin is None
        assert d.simulacao_final_com_data is None
        assert d.utiliza_gerenciamento_pls is None
        assert d.comunicacao_dois_niveis is None
        assert d.armazenamento_local_arquivos_temporarios is None
        assert d.alocacao_memoria_ena is None
        assert d.alocacao_memoria_cortes is None
        assert d.sar is None
        assert d.cvar is None
        assert d.considera_zsup_min_convergencia is None
        assert d.desconsidera_vazao_minima is None
        assert d.restricoes_eletricas is None
        assert d.selecao_de_cortes_backward is None
        assert d.selecao_de_cortes_forward is None
        assert d.janela_de_cortes is None
        assert d.considera_reamostragem_cenarios is None
        assert d.tipo_reamostragem_cenarios is None
        assert d.passo_reamostragem_cenarios is None
        assert d.converge_no_zero is None
        assert d.consulta_fcf is None
        assert d.impressao_ena is None
        assert d.impressao_cortes_ativos_sim_final is None
        assert d.representacao_agregacao is None
        assert d.matriz_correlacao_espacial is None
        assert d.desconsidera_convergencia_estatistica is None
        assert d.momento_reamostragem is None
        assert d.mantem_arquivos_energias is None
        assert d.inicio_teste_convergencia is None
        assert d.sazonaliza_vmint is None
        assert d.sazonaliza_vmaxt is None
        assert d.sazonaliza_vminp is None
        assert d.sazonaliza_cfuga_cmont is None
        assert d.restricoes_emissao_gee is None
        assert d.consideracao_media_anual_afluencias is None
        assert d.reducao_automatica_ordem is None
        assert d.restricoes_fornecimento_gas is None
        assert d.memoria_calculo_cortes is None
        assert d.considera_geracao_eolica is None
        assert d.penalidade_corte_geracao_eolica is None
        assert d.compensacao_correlacao_cruzada is None
        assert d.restricao_defluencia is None
        assert d.restricao_turbinamento is None
        assert d.aproveitamento_bases_backward is None
        assert d.impressao_estados_geracao_cortes is None
        assert d.semente_forward is None
        assert d.semente_backward is None
        assert d.restricao_lpp_turbinamento_maximo_ree is None
        assert d.restricao_lpp_defluencia_maxima_ree is None
        assert d.restricao_lpp_turbinamento_maximo_uhe is None
        assert d.restricao_lpp_defluencia_maxima_uhe is None
        assert d.restricoes_eletricas_especiais is None
        assert d.funcao_producao_uhe is None


def test_atributos_encontrados_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.nome_caso is not None
        assert d.tipo_execucao is not None
        assert d.duracao_periodo is not None
        assert d.num_anos_estudo is not None
        assert d.mes_inicio_pre_estudo is not None
        assert d.mes_inicio_estudo is not None
        assert d.ano_inicio_estudo is not None
        assert d.num_anos_pre_estudo is not None
        assert d.num_anos_pos_estudo is not None
        assert d.num_anos_pos_sim_final is not None
        assert d.imprime_dados is not None
        assert d.imprime_mercados is not None
        assert d.imprime_energias is not None
        assert d.imprime_modelo_estocastico is not None
        assert d.imprime_subsistema is not None
        assert d.num_max_iteracoes is not None
        assert d.num_forwards is not None
        assert d.num_aberturas is not None
        assert d.num_series_sinteticas is not None
        assert d.ordem_maxima_parp is not None
        assert d.ano_inicial_historico is not None
        assert d.tamanho_registro_arquivo_historico is not None
        assert d.calcula_volume_inicial is not None
        assert d.volume_inicial_subsistema != [
            None,
            None,
            None,
            None,
            None,
        ]
        assert d.tolerancia is not None
        assert d.taxa_de_desconto is not None
        assert d.tipo_simulacao_final is not None
        assert d.agregacao_simulacao_final is not None
        assert d.impressao_operacao is not None
        assert d.impressao_convergencia is not None
        assert d.intervalo_para_gravar is not None
        assert d.num_minimo_iteracoes is not None
        assert d.racionamento_preventivo is not None
        assert d.num_anos_manutencao_utes is not None
        assert d.considera_tendencia_hidrologica_calculo_politica is not None
        assert d.considera_tendencia_hidrologica_sim_final is not None
        assert d.restricao_itaipu is not None
        assert d.bid is not None
        assert d.perdas_rede_transmissao is not None
        assert d.el_nino is not None
        assert d.enso is not None
        assert d.duracao_por_patamar is not None
        assert d.outros_usos_da_agua is not None
        assert d.correcao_desvio is not None
        assert d.curva_aversao is not None
        assert d.tipo_geracao_enas is not None
        assert d.primeira_profundidade_risco_deficit is not None
        assert d.segunda_profundidade_risco_deficit is not None
        assert d.iteracao_para_simulacao_final is not None
        assert d.agrupamento_livre is not None
        assert d.equalizacao_penal_intercambio is not None
        assert d.representacao_submotorizacao is not None
        assert d.ordenacao_automatica is not None
        assert d.considera_carga_adicional is not None
        assert d.delta_zsup is not None
        assert d.delta_zinf is not None
        assert d.deltas_consecutivos is not None
        assert d.despacho_antecipado_gnl is not None
        assert d.modif_automatica_adterm is not None
        assert d.considera_ghmin is not None
        assert d.simulacao_final_com_data is not None
        assert d.utiliza_gerenciamento_pls is not None
        assert d.comunicacao_dois_niveis is not None
        assert d.armazenamento_local_arquivos_temporarios is not None
        assert d.alocacao_memoria_ena is not None
        assert d.alocacao_memoria_cortes is not None
        assert d.sar is not None
        assert d.cvar is not None
        assert d.considera_zsup_min_convergencia is not None
        assert d.desconsidera_vazao_minima is not None
        assert d.restricoes_eletricas is not None
        assert d.selecao_de_cortes_backward is not None
        assert d.selecao_de_cortes_forward is not None
        assert d.janela_de_cortes is not None
        assert d.considera_reamostragem_cenarios is not None
        assert d.tipo_reamostragem_cenarios is not None
        assert d.passo_reamostragem_cenarios is not None
        assert d.converge_no_zero is not None
        assert d.consulta_fcf is not None
        assert d.impressao_ena is not None
        assert d.impressao_cortes_ativos_sim_final is not None
        assert d.representacao_agregacao is not None
        assert d.matriz_correlacao_espacial is not None
        assert d.desconsidera_convergencia_estatistica is not None
        assert d.momento_reamostragem is not None
        assert d.mantem_arquivos_energias is not None
        assert d.inicio_teste_convergencia is not None
        assert d.sazonaliza_vmint is not None
        assert d.sazonaliza_vmaxt is not None
        assert d.sazonaliza_vminp is not None
        assert d.sazonaliza_cfuga_cmont is not None
        assert d.restricoes_emissao_gee is not None
        assert d.consideracao_media_anual_afluencias is not None
        assert d.reducao_automatica_ordem is not None
        assert d.restricoes_fornecimento_gas is not None
        assert d.memoria_calculo_cortes is not None
        assert d.considera_geracao_eolica is not None
        assert d.penalidade_corte_geracao_eolica is not None
        assert d.compensacao_correlacao_cruzada is not None
        assert d.restricao_defluencia is not None
        assert d.restricao_turbinamento is not None
        assert d.aproveitamento_bases_backward is not None
        assert d.impressao_estados_geracao_cortes is not None
        assert d.semente_forward is not None
        assert d.semente_backward is not None
        assert d.restricao_lpp_turbinamento_maximo_ree is not None
        assert d.restricao_lpp_defluencia_maxima_ree is not None
        assert d.restricao_lpp_turbinamento_maximo_uhe is not None
        assert d.restricao_lpp_defluencia_maxima_uhe is not None
        assert d.restricoes_eletricas_especiais is not None
        assert d.funcao_producao_uhe is not None


def test_nome_caso_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.nome_caso == (
            "PMO JANEIRO - 2021  22/12/2020 12:43:55  Niveis"
            + " para 26/12 NW Versao 27.5_CPAMP"
        )
        novo_valor = "Teste"
        d.nome_caso = novo_valor
        assert d.nome_caso == novo_valor


def test_tipo_execucao_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.tipo_execucao == 1
        novo_valor = 0
        d.tipo_execucao = novo_valor
        assert d.tipo_execucao == novo_valor


def test_duracao_periodo_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.duracao_periodo == 1
        novo_valor = 0
        d.duracao_periodo = novo_valor
        assert d.duracao_periodo == novo_valor


def test_num_anos_estudo_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_anos_estudo == 5
        novo_valor = 0
        d.num_anos_estudo = novo_valor
        assert d.num_anos_estudo == novo_valor


def test_mes_inicio_pre_estudo_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.mes_inicio_pre_estudo == 1
        novo_valor = 0
        d.mes_inicio_pre_estudo = novo_valor
        assert d.mes_inicio_pre_estudo == novo_valor


def test_mes_inicio_estudo_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.mes_inicio_estudo == 1
        novo_valor = 0
        d.mes_inicio_estudo = novo_valor
        assert d.mes_inicio_estudo == novo_valor


def test_ano_inicio_estudo_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.ano_inicio_estudo == 2021
        novo_valor = 0
        d.ano_inicio_estudo = novo_valor
        assert d.ano_inicio_estudo == novo_valor


def test_num_anos_pre_estudo_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_anos_pre_estudo == 0
        novo_valor = 5
        d.num_anos_pre_estudo = novo_valor
        assert d.num_anos_pre_estudo == novo_valor


def test_num_anos_pos_estudo_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_anos_pos_estudo == 5
        novo_valor = 0
        d.num_anos_pos_estudo = novo_valor
        assert d.num_anos_pos_estudo == novo_valor


def test_num_anos_pos_sim_final_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_anos_pos_sim_final == 0
        novo_valor = 1
        d.num_anos_pos_sim_final = novo_valor
        assert d.num_anos_pos_sim_final == novo_valor


def test_imprime_dados_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.imprime_dados == 1
        novo_valor = 0
        d.imprime_dados = novo_valor
        assert d.imprime_dados == novo_valor


def test_imprime_mercados_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.imprime_mercados == 1
        novo_valor = 0
        d.imprime_mercados = novo_valor
        assert d.imprime_mercados == novo_valor


def test_imprime_energias_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.imprime_energias == 1
        novo_valor = 0
        d.imprime_energias = novo_valor
        assert d.imprime_energias == novo_valor


def test_imprime_modelo_estocastico_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.imprime_modelo_estocastico == 1
        novo_valor = 0
        d.imprime_modelo_estocastico = novo_valor
        assert d.imprime_modelo_estocastico == novo_valor


def test_imprime_subsistema_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.imprime_subsistema == 1
        novo_valor = 0
        d.imprime_subsistema = novo_valor
        assert d.imprime_subsistema == novo_valor


def test_num_max_iteracoes_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_max_iteracoes == 45
        novo_valor = 0
        d.num_max_iteracoes = novo_valor
        assert d.num_max_iteracoes == novo_valor


def test_num_forwards_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_forwards == 200
        novo_valor = 0
        d.num_forwards = novo_valor
        assert d.num_forwards == novo_valor


def test_num_aberturas_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_aberturas == 20
        novo_valor = 0
        d.num_aberturas = novo_valor
        assert d.num_aberturas == novo_valor


def test_num_series_sinteticas_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_series_sinteticas == 2000
        novo_valor = 0
        d.num_series_sinteticas = novo_valor
        assert d.num_series_sinteticas == novo_valor


def test_ordem_maxima_parp_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.ordem_maxima_parp == 6
        novo_valor = 0
        d.ordem_maxima_parp = novo_valor
        assert d.ordem_maxima_parp == novo_valor


def test_ano_inicial_historico_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.ano_inicial_historico == 1931
        novo_valor = 0
        d.ano_inicial_historico = novo_valor
        assert d.ano_inicial_historico == novo_valor


def test_tamanho_registro_arquivo_historico_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.tamanho_registro_arquivo_historico == 0
        novo_valor = 1
        d.tamanho_registro_arquivo_historico = novo_valor
        assert d.tamanho_registro_arquivo_historico == novo_valor


def test_calcula_volume_inicial_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.calcula_volume_inicial == 1
        novo_valor = 0
        d.calcula_volume_inicial = novo_valor
        assert d.calcula_volume_inicial == novo_valor


def test_volume_inicial_subsistema_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.volume_inicial_subsistema == [0.0, 0.0, 0.0, 0.0, 0.0]
        novo_valor = [1.0, 1.0, 1.0, 1.0, 1.0]
        d.volume_inicial_subsistema = novo_valor
        assert d.volume_inicial_subsistema == novo_valor


def test_tolerancia_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.tolerancia == 95.0
        novo_valor = 0.0
        d.tolerancia = novo_valor
        assert d.tolerancia == novo_valor


def test_taxa_de_desconto_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.taxa_de_desconto == 12.0
        novo_valor = 0.0
        d.taxa_de_desconto = novo_valor
        assert d.taxa_de_desconto == novo_valor


def test_tipo_simulacao_final_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.tipo_simulacao_final == 1
        novo_valor = 0
        d.tipo_simulacao_final = novo_valor
        assert d.tipo_simulacao_final == novo_valor


def test_agregacao_simulacao_final_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.agregacao_simulacao_final == 1
        novo_valor = 0
        d.agregacao_simulacao_final = novo_valor
        assert d.agregacao_simulacao_final == novo_valor


def test_impressao_operacao_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.impressao_operacao == 1
        novo_valor = 0
        d.impressao_operacao = novo_valor
        assert d.impressao_operacao == novo_valor


def test_impressao_convergencia_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.impressao_convergencia == 1
        novo_valor = 0
        d.impressao_convergencia = novo_valor
        assert d.impressao_convergencia == novo_valor


def test_intervalo_para_gravar_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.intervalo_para_gravar == 1
        novo_valor = 0
        d.intervalo_para_gravar = novo_valor
        assert d.intervalo_para_gravar == novo_valor


def test_num_minimo_iteracoes_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_minimo_iteracoes == 30
        novo_valor = 0
        d.num_minimo_iteracoes = novo_valor
        assert d.num_minimo_iteracoes == novo_valor


def test_racionamento_preventivo_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.racionamento_preventivo == 0
        novo_valor = 1
        d.racionamento_preventivo = novo_valor
        assert d.racionamento_preventivo == novo_valor


def test_num_anos_manutencao_utes_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.num_anos_manutencao_utes == 1
        novo_valor = 0
        d.num_anos_manutencao_utes = novo_valor
        assert d.num_anos_manutencao_utes == novo_valor


def test_tendencia_hidrologica_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.considera_tendencia_hidrologica_calculo_politica == 2
        assert d.considera_tendencia_hidrologica_sim_final == 2
        novo_valor = 0
        d.considera_tendencia_hidrologica_calculo_politica = novo_valor
        assert d.considera_tendencia_hidrologica_calculo_politica == novo_valor
        d.considera_tendencia_hidrologica_sim_final = novo_valor
        assert d.considera_tendencia_hidrologica_sim_final == novo_valor


def test_restricao_itaipu_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricao_itaipu == 0
        novo_valor = 1
        d.restricao_itaipu = novo_valor
        assert d.restricao_itaipu == novo_valor


def test_bid_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.bid == 0
        novo_valor = 1
        d.bid = novo_valor
        assert d.bid == novo_valor


def test_perdas_rede_transmissao_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.perdas_rede_transmissao == 0
        novo_valor = 1
        d.perdas_rede_transmissao = novo_valor
        assert d.perdas_rede_transmissao == novo_valor


def test_el_nino_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.el_nino == 0
        novo_valor = 1
        d.el_nino = novo_valor
        assert d.el_nino == novo_valor


def test_enso_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.enso == 0
        novo_valor = 1
        d.enso = novo_valor
        assert d.enso == novo_valor


def test_duracao_por_patamar_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.duracao_por_patamar == 1
        novo_valor = 0
        d.duracao_por_patamar = novo_valor
        assert d.duracao_por_patamar == novo_valor


def test_outros_usos_da_agua_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.outros_usos_da_agua == 1
        novo_valor = 0
        d.outros_usos_da_agua = novo_valor
        assert d.outros_usos_da_agua == novo_valor


def test_correcao_desvio_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.correcao_desvio == 1
        novo_valor = 0
        d.correcao_desvio = novo_valor
        assert d.correcao_desvio == novo_valor


def test_curva_aversao_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.curva_aversao == 1
        novo_valor = 0
        d.curva_aversao = novo_valor
        assert d.curva_aversao == novo_valor


def test_tipo_geracao_enas_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.tipo_geracao_enas == 0
        novo_valor = 1
        d.tipo_geracao_enas = novo_valor
        assert d.tipo_geracao_enas == novo_valor


def test_risco_deficit_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.primeira_profundidade_risco_deficit == 1.0
        assert d.segunda_profundidade_risco_deficit == 2.5
        novo_valor = 0.0
        d.primeira_profundidade_risco_deficit = novo_valor
        assert d.primeira_profundidade_risco_deficit == novo_valor
        d.segunda_profundidade_risco_deficit = novo_valor
        assert d.segunda_profundidade_risco_deficit == novo_valor


def test_iteracao_para_simulacao_final_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.iteracao_para_simulacao_final == 0
        novo_valor = 1
        d.iteracao_para_simulacao_final = novo_valor
        assert d.iteracao_para_simulacao_final == novo_valor


def test_agrupamento_livre_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.agrupamento_livre == 1
        novo_valor = 0
        d.agrupamento_livre = novo_valor
        assert d.agrupamento_livre == novo_valor


def test_equalizacao_penal_intercambio_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.equalizacao_penal_intercambio == 1
        novo_valor = 0
        d.equalizacao_penal_intercambio = novo_valor
        assert d.equalizacao_penal_intercambio == novo_valor


def test_representacao_submotorizacao_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.representacao_submotorizacao == 2
        novo_valor = 0
        d.representacao_submotorizacao = novo_valor
        assert d.representacao_submotorizacao == novo_valor


def test_ordenacao_automatica_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.ordenacao_automatica == 0
        novo_valor = 1
        d.ordenacao_automatica = novo_valor
        assert d.ordenacao_automatica == novo_valor


def test_considera_carga_adicional_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.considera_carga_adicional == 1
        novo_valor = 0
        d.considera_carga_adicional = novo_valor
        assert d.considera_carga_adicional == novo_valor


def test_delta_zsup_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.delta_zsup == 10
        novo_valor = 0.0
        d.delta_zsup = novo_valor
        assert d.delta_zsup == novo_valor


def test_delta_zinf_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.delta_zinf == 0.2
        novo_valor = 0.0
        d.delta_zinf = novo_valor
        assert d.delta_zinf == novo_valor


def test_deltas_consecutivos_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.deltas_consecutivos == 3
        novo_valor = 0
        d.deltas_consecutivos = novo_valor
        assert d.deltas_consecutivos == novo_valor


def test_despacho_antecipado_gnl_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.despacho_antecipado_gnl == 1
        novo_valor = 0
        d.despacho_antecipado_gnl = novo_valor
        assert d.despacho_antecipado_gnl == novo_valor


def test_modif_automatica_adterm_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.modif_automatica_adterm == 1
        novo_valor = 0
        d.modif_automatica_adterm = novo_valor
        assert d.modif_automatica_adterm == novo_valor


def test_considera_ghmin_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.considera_ghmin == 1
        novo_valor = 0
        d.considera_ghmin = novo_valor
        assert d.considera_ghmin == novo_valor


def test_simulacao_final_com_data_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.simulacao_final_com_data == 0
        novo_valor = 1
        d.simulacao_final_com_data = novo_valor
        assert d.simulacao_final_com_data == novo_valor


def test_gerenciamento_pls_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.utiliza_gerenciamento_pls == 0
        assert d.comunicacao_dois_niveis == 0
        assert d.armazenamento_local_arquivos_temporarios == 0
        assert d.alocacao_memoria_ena == 0
        assert d.alocacao_memoria_cortes == 0
        novo_valor = 1
        d.utiliza_gerenciamento_pls = novo_valor
        assert d.utiliza_gerenciamento_pls == novo_valor
        d.comunicacao_dois_niveis = novo_valor
        assert d.comunicacao_dois_niveis == novo_valor
        d.armazenamento_local_arquivos_temporarios = novo_valor
        assert d.armazenamento_local_arquivos_temporarios == novo_valor
        d.alocacao_memoria_ena = novo_valor
        assert d.alocacao_memoria_ena == novo_valor
        d.alocacao_memoria_cortes = novo_valor
        assert d.alocacao_memoria_cortes == novo_valor


def test_sar_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.sar == 0
        novo_valor = 1
        d.sar = novo_valor
        assert d.sar == novo_valor


def test_cvar_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.cvar == 1
        novo_valor = 0
        d.cvar = novo_valor
        assert d.cvar == novo_valor


def test_considera_zsup_min_convergencia_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.considera_zsup_min_convergencia == 0
        novo_valor = 0
        d.considera_zsup_min_convergencia = novo_valor
        assert d.considera_zsup_min_convergencia == novo_valor


def test_desconsidera_vazao_minima_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.desconsidera_vazao_minima == 0
        novo_valor = 1
        d.desconsidera_vazao_minima = novo_valor
        assert d.desconsidera_vazao_minima == novo_valor


def test_restricoes_eletricas_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricoes_eletricas == 1
        novo_valor = 0
        d.restricoes_eletricas = novo_valor
        assert d.restricoes_eletricas == novo_valor


def test_selecao_de_cortes_backward_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.selecao_de_cortes_backward == 1
        novo_valor = 0
        d.selecao_de_cortes_backward = novo_valor
        assert d.selecao_de_cortes_backward == novo_valor


def test_selecao_de_cortes_forward_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.selecao_de_cortes_forward == 1
        novo_valor = 0
        d.selecao_de_cortes_forward = novo_valor
        assert d.selecao_de_cortes_forward == novo_valor


def test_janela_de_cortes_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.janela_de_cortes == 0
        novo_valor = 1
        d.janela_de_cortes = novo_valor
        assert d.janela_de_cortes == novo_valor


def test_reamostragem_cenarios_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.considera_reamostragem_cenarios == 1
        assert d.tipo_reamostragem_cenarios == 1
        assert d.passo_reamostragem_cenarios == 1
        novo_valor = 0
        d.considera_reamostragem_cenarios = novo_valor
        assert d.considera_reamostragem_cenarios == novo_valor
        d.tipo_reamostragem_cenarios = novo_valor
        assert d.tipo_reamostragem_cenarios == novo_valor
        d.passo_reamostragem_cenarios = novo_valor
        assert d.passo_reamostragem_cenarios == novo_valor


def test_converge_no_zero_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.converge_no_zero == 0
        novo_valor = 1
        d.converge_no_zero = novo_valor
        assert d.converge_no_zero == novo_valor


def test_consulta_fcf_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.consulta_fcf == 0
        novo_valor = 1
        d.consulta_fcf = novo_valor
        assert d.consulta_fcf == novo_valor


def test_impressao_ena_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.impressao_ena == 1
        novo_valor = 0
        d.impressao_ena = novo_valor
        assert d.impressao_ena == novo_valor


def test_impressao_cortes_ativos_sim_final_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.impressao_cortes_ativos_sim_final == 0
        novo_valor = 1
        d.impressao_cortes_ativos_sim_final = novo_valor
        assert d.impressao_cortes_ativos_sim_final == novo_valor


def test_representacao_agregacao_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.representacao_agregacao == 1
        novo_valor = 0
        d.representacao_agregacao = novo_valor
        assert d.representacao_agregacao == novo_valor


def test_matriz_correlacao_espacial_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.matriz_correlacao_espacial == 1
        novo_valor = 0
        d.matriz_correlacao_espacial = novo_valor
        assert d.matriz_correlacao_espacial == novo_valor


def test_desconsidera_convergencia_estatistica_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.desconsidera_convergencia_estatistica == 1
        novo_valor = 0
        d.desconsidera_convergencia_estatistica = novo_valor
        assert d.desconsidera_convergencia_estatistica == novo_valor


def test_momento_reamostragem_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.momento_reamostragem == 1
        novo_valor = 0
        d.momento_reamostragem = novo_valor
        assert d.momento_reamostragem == novo_valor


def test_mantem_arquivos_energias_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.mantem_arquivos_energias == 0
        novo_valor = 1
        d.mantem_arquivos_energias = novo_valor
        assert d.mantem_arquivos_energias == novo_valor


def test_inicio_teste_convergencia_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.inicio_teste_convergencia == 1
        novo_valor = 0
        d.inicio_teste_convergencia = novo_valor
        assert d.inicio_teste_convergencia == novo_valor


def test_sazonaliza_vmint_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.sazonaliza_vmint == 0
        novo_valor = 1
        d.sazonaliza_vmint = novo_valor
        assert d.sazonaliza_vmint == novo_valor


def test_sazonaliza_vmaxt_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.sazonaliza_vmaxt == 0
        novo_valor = 1
        d.sazonaliza_vmaxt = novo_valor
        assert d.sazonaliza_vmaxt == novo_valor


def test_sazonaliza_vminp_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.sazonaliza_vminp == 0
        novo_valor = 1
        d.sazonaliza_vminp = novo_valor
        assert d.sazonaliza_vminp == novo_valor


def test_sazonaliza_cfuga_cmont_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.sazonaliza_cfuga_cmont == 0
        novo_valor = 1
        d.sazonaliza_cfuga_cmont = novo_valor
        assert d.sazonaliza_cfuga_cmont == novo_valor


def test_restricoes_emissao_gee_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricoes_emissao_gee == 0
        novo_valor = 1
        d.restricoes_emissao_gee = novo_valor
        assert d.restricoes_emissao_gee == novo_valor


def test_afluencia_anual_parp_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.consideracao_media_anual_afluencias == 3
        assert d.reducao_automatica_ordem == 0
        novo_valor = 1
        d.consideracao_media_anual_afluencias = novo_valor
        assert d.consideracao_media_anual_afluencias == novo_valor
        d.reducao_automatica_ordem = novo_valor
        assert d.reducao_automatica_ordem == novo_valor


def test_restricoes_fornecimento_gas_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricoes_fornecimento_gas == 0
        novo_valor = 1
        d.restricoes_fornecimento_gas = novo_valor
        assert d.restricoes_fornecimento_gas == novo_valor


def test_memoria_calculo_cortes_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.memoria_calculo_cortes == 0
        novo_valor = 1
        d.memoria_calculo_cortes = novo_valor
        assert d.memoria_calculo_cortes == novo_valor


def test_considera_geracao_eolica_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.considera_geracao_eolica == 1
        novo_valor = 0
        d.considera_geracao_eolica = novo_valor
        assert d.considera_geracao_eolica == novo_valor


def test_penalidade_corte_geracao_eolica_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.penalidade_corte_geracao_eolica == 0.0063
        novo_valor = 1.0
        d.penalidade_corte_geracao_eolica = novo_valor
        assert d.penalidade_corte_geracao_eolica == novo_valor


def test_compensacao_correlacao_cruzada_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.compensacao_correlacao_cruzada == 1
        novo_valor = 0
        d.compensacao_correlacao_cruzada = novo_valor
        assert d.compensacao_correlacao_cruzada == novo_valor


def test_restricao_turbinamento_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricao_turbinamento == 1
        novo_valor = 0
        d.restricao_turbinamento = novo_valor
        assert d.restricao_turbinamento == novo_valor


def test_restricao_defluencia_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricao_defluencia == 1
        novo_valor = 0
        d.restricao_defluencia = novo_valor
        assert d.restricao_defluencia == novo_valor


def test_aproveitamento_base_pls_backward_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.aproveitamento_bases_backward == 1
        novo_valor = 0
        d.aproveitamento_bases_backward = novo_valor
        assert d.aproveitamento_bases_backward == novo_valor


def test_impressao_estados_geracao_cortes_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.impressao_estados_geracao_cortes == 1
        novo_valor = 0
        d.impressao_estados_geracao_cortes = novo_valor
        assert d.impressao_estados_geracao_cortes == novo_valor


def test_semente_forward_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.semente_forward == 0
        novo_valor = 1000
        d.semente_forward = novo_valor
        assert d.semente_forward == novo_valor


def test_semente_backward_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.semente_backward == 0
        novo_valor = 1000
        d.semente_backward = novo_valor
        assert d.semente_backward == novo_valor


def test_restricao_lpp_turbinamento_maximo_ree_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricao_lpp_turbinamento_maximo_ree == 1
        novo_valor = 0
        d.restricao_lpp_turbinamento_maximo_ree = novo_valor
        assert d.restricao_lpp_turbinamento_maximo_ree == novo_valor


def test_restricao_lpp_defluencia_maxima_ree_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricao_lpp_defluencia_maxima_ree == 1
        novo_valor = 0
        d.restricao_lpp_defluencia_maxima_ree = novo_valor
        assert d.restricao_lpp_defluencia_maxima_ree == novo_valor


def test_restricao_lpp_turbinamento_maximo_uhe_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricao_lpp_turbinamento_maximo_uhe == 1
        novo_valor = 0
        d.restricao_lpp_turbinamento_maximo_uhe = novo_valor
        assert d.restricao_lpp_turbinamento_maximo_uhe == novo_valor


def test_restricao_lpp_defluencia_maxima_uhe_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricao_lpp_defluencia_maxima_uhe == 1
        novo_valor = 0
        d.restricao_lpp_defluencia_maxima_uhe = novo_valor
        assert d.restricao_lpp_defluencia_maxima_uhe == novo_valor


def test_restricoes_eletricas_especiais():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.restricoes_eletricas_especiais == 0
        novo_valor = 1
        d.restricoes_eletricas_especiais = novo_valor
        assert d.restricoes_eletricas_especiais == novo_valor


def test_funcao_producao_uhe():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.funcao_producao_uhe == 0
        novo_valor = 1
        d.funcao_producao_uhe = novo_valor
        assert d.funcao_producao_uhe == novo_valor


def test_eq_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d1 = DGer.le_arquivo("")
        d2 = DGer.le_arquivo("")
        assert d1 == d2


def test_neq_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d1 = DGer.le_arquivo("")
        d2 = DGer.le_arquivo("")
        d2.nome_caso = "Teste"
        assert d1 != d2


def test_leitura_escrita_dger():
    m_leitura: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m_leitura):
        d1 = DGer.le_arquivo("")
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        d1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(2, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        d2 = DGer.le_arquivo("")
        assert d1 == d2
