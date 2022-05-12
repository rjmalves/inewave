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
        assert d.volume_inicial_por_subsistema == [None, None, None, None, None]
        assert d.tolerancia is None
        assert d.taxa_de_desconto is None
        assert d.tipo_simulacao_final is None
        assert d.impressao_operacao is None
        assert d.impressao_convergencia is None
        assert d.intervalo_para_gravar is None
        assert d.num_minimo_iteracoes is None
        assert d.racionamento_preventivo is None
        assert d.num_anos_manutencao_utes is None
        assert d.tendencia_hidrologica == [None, None]
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
        assert d.risco_deficit == [None, None]
        assert d.iteracao_para_simulacao_final is None
        assert d.agrupamento_livre is None
        assert d.equalizacao_penal_itercambio is None
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
        assert d.gerenciamento_pls == [None, None, None, None, None]
        assert d.sar is None
        assert d.cvar is None
        assert d.considera_zsup_min_convergencia is None
        assert d.desconsidera_vazao_minima is None
        assert d.restricoes_eletricas is None
        assert d.selecao_de_cortes is None
        assert d.janela_de_cortes is None
        assert d.reamostragem_cenarios == [None, None, None]
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
        assert d.afluencia_anual_parp == [None, None]
        assert d.restricoes_fornecimento_gas is None
        assert d.memoria_calculo_cortes is None
        assert d.considera_geracao_eolica is None
        assert d.penalidade_corte_geracao_eolica is None
        assert d.compensacao_correlacao_cruzada is None


def test_atributos_encontrados_dger():
    m: MagicMock = mock_open(read_data="".join(MockDger))
    with patch("builtins.open", m):
        d = DGer.le_arquivo("")
        assert d.nome_caso != None
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
        assert d.volume_inicial_por_subsistema != [None, None, None, None, None]
        assert d.tolerancia is not None
        assert d.taxa_de_desconto is not None
        assert d.tipo_simulacao_final is not None
        assert d.impressao_operacao is not None
        assert d.impressao_convergencia is not None
        assert d.intervalo_para_gravar is not None
        assert d.num_minimo_iteracoes is not None
        assert d.racionamento_preventivo is not None
        assert d.num_anos_manutencao_utes is not None
        assert d.tendencia_hidrologica != [None, None]
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
        assert d.risco_deficit != [None, None]
        assert d.iteracao_para_simulacao_final is not None
        assert d.agrupamento_livre is not None
        assert d.equalizacao_penal_itercambio is not None
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
        assert d.gerenciamento_pls != [None, None, None, None, None]
        assert d.sar is not None
        assert d.cvar is not None
        assert d.considera_zsup_min_convergencia is not None
        assert d.desconsidera_vazao_minima is not None
        assert d.restricoes_eletricas is not None
        assert d.selecao_de_cortes is not None
        assert d.janela_de_cortes is not None
        assert d.reamostragem_cenarios != [None, None, None]
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
        assert d.afluencia_anual_parp is not None
        assert d.restricoes_fornecimento_gas is not None
        assert d.memoria_calculo_cortes is not None
        assert d.considera_geracao_eolica is not None
        assert d.penalidade_corte_geracao_eolica is not None
        assert d.compensacao_correlacao_cruzada is not None


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
        linhas_escritas = [chamadas[i].args[0] for i in range(3, len(chamadas) - 1)]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        d2 = DGer.le_arquivo("")
        for b1, b2 in zip(d1.data, d2.data):
            if b1 != b2:
                print(b1.__class__)
                print(b1.data)
                print(b2.data)
        assert d1 == d2


# def test_leitura():
#     assert len(dger.nome_caso) > 0


# def test_nome_caso():
#     nome = (
#         "PMO JANEIRO - 2021  22/12/2020 12:43:55  Niveis "
#         + "para 26/12 NW Versao 27.5_CPAMP"
#     )
#     assert dger.nome_caso == nome


# def test_tipo_execucao():
#     assert dger.tipo_execucao == 1


# def test_duracao_periodo():
#     assert dger.duracao_periodo == 1


# def test_num_anos_estudo():
#     assert dger.num_anos_estudo == 5


# def test_mes_inicio_pre():
#     assert dger.mes_inicio_pre_estudo == 1


# def test_mes_inicio_estudo():
#     assert dger.mes_inicio_estudo == 1


# def test_ano_inicio_estudo():
#     assert dger.ano_inicio_estudo == 2021


# def test_num_anos_pre():
#     assert dger.num_anos_pre_estudo == 0


# def test_num_anos_pos():
#     assert dger.num_anos_pos_estudo == 5


# def test_num_anos_pos_final():
#     assert dger.num_anos_pos_sim_final == 0


# def test_imprime_dados():
#     assert dger.imprime_dados == 1


# def test_imprime_mercados():
#     assert dger.imprime_mercados == 1


# def test_imprime_energias():
#     assert dger.imprime_energias == 1


# def test_imprime_modelo_estocastico():
#     assert dger.imprime_modelo_estocastico == 1


# def test_imprime_subsistema():
#     assert dger.imprime_subsistema == 1


# def test_num_max_iteracoes():
#     assert dger.num_max_iteracoes == 45


# def test_num_forwards():
#     assert dger.num_forwards == 200


# def test_num_aberturas():
#     assert dger.num_aberturas == 20


# def test_num_series_sinteticas():
#     assert dger.num_series_sinteticas == 2000


# def test_ordem_maxima_parp():
#     assert dger.ordem_maxima_parp == 6


# def test_ano_inicial_historico():
#     assert dger.ano_inicial_historico == [1931, 0]


# def test_calcula_volume_inicial():
#     assert dger.calcula_volume_inicial == 1


# def test_volume_inicial_por_subsistema():
#     assert dger.volume_inicial_por_subsistema == [0.0, 0.0, 0.0, 0.0, 0.0]


# def test_tolerancia():
#     assert dger.tolerancia == 95.0


# def test_taxa_de_desconto():
#     assert dger.taxa_de_desconto == 12.0


# def test_tipo_simulacao_final():
#     assert dger.tipo_simulacao_final == 1


# def test_impressao_operacao():
#     assert dger.impressao_operacao == 1


# def test_impressao_convergencia():
#     assert dger.impressao_convergencia == 1


# def test_intervalo_para_gravar():
#     assert dger.intervalo_para_gravar == 1


# def test_num_minimo_iteracoes():
#     assert dger.num_minimo_iteracoes == 30


# def test_racionamento_preventivo():
#     assert dger.racionamento_preventivo == 0


# def test_num_anos_manutencao_utes():
#     assert dger.num_anos_manutencao_utes == 1


# def test_tendencia_hidrologica():
#     assert dger.tendencia_hidrologica == [2, 2]


# def test_restricao_itaipu():
#     assert dger.restricao_itaipu == 0


# def test_bid():
#     assert dger.bid == 0


# def test_perdas_rede_transmissao():
#     assert dger.perdas_rede_transmissao == 0


# def test_el_nino():
#     assert dger.el_nino == 0


# def test_enso():
#     assert dger.enso == 0


# def test_duracao_por_patamar():
#     assert dger.duracao_por_patamar == 1


# def test_outros_usos_da_agua():
#     assert dger.outros_usos_da_agua == 1


# def test_correcao_desvio():
#     assert dger.correcao_desvio == 1


# def test_curva_aversao():
#     assert dger.curva_aversao == 1


# def test_tipo_geracao_enas():
#     assert dger.tipo_geracao_enas == 0


# def test_risco_deficit():
#     assert dger.risco_deficit == [1.0, 2.5]


# def test_iteracao_para_simulacao_final():
#     assert dger.iteracao_para_simulacao_final == 0


# def test_agrupamento_livre():
#     assert dger.agrupamento_livre == 1


# def test_equalizacao_penal_itercambio():
#     assert dger.equalizacao_penal_itercambio == 1


# def test_representacao_submotorizacao():
#     assert dger.representacao_submotorizacao == 2


# def test_ordenacao_automatica():
#     assert dger.ordenacao_automatica == 0


# def test_considera_carga_adicional():
#     assert dger.considera_carga_adicional == 1


# def test_delta_zsup():
#     assert dger.delta_zsup == 10


# def test_delta_zinf():
#     assert dger.delta_zinf == 0.2


# def test_deltas_consecutivos():
#     assert dger.deltas_consecutivos == 3


# def test_despacho_antecipado_gnl():
#     assert dger.despacho_antecipado_gnl == 1


# def test_modif_automatica_adterm():
#     assert dger.modif_automatica_adterm == 1


# def test_considera_ghmin():
#     assert dger.considera_ghmin == 1


# def test_simulacao_final_com_data():
#     assert dger.simulacao_final_com_data == 0


# def test_gerenciamento_pls():
#     assert dger.gerenciamento_pls == [0, 0, 0, 0, 0]


# def test_sar():
#     assert dger.sar == 0


# def test_cvar():
#     assert dger.cvar == 1


# def test_considera_zsup_min_convergencia():
#     assert dger.considera_zsup_min_convergencia == 0


# def test_desconsidera_vazao_minima():
#     assert dger.desconsidera_vazao_minima == 0


# def test_restricoes_eletricas():
#     assert dger.restricoes_eletricas == 1


# def test_selecao_de_cortes():
#     assert dger.selecao_de_cortes == 1


# def test_janela_de_cortes():
#     assert dger.janela_de_cortes == 0


# def test_reamostragem():
#     assert dger.reamostragem_cenarios == [1, 1, 1]


# def test_converge_no_zero():
#     assert dger.converge_no_zero == 0


# def test_consulta_fcf():
#     assert dger.consulta_fcf == 0


# def test_impressao_ena():
#     assert dger.impressao_ena == 1


# def test_impressao_cortes_ativos_sim_final():
#     assert dger.impressao_cortes_ativos_sim_final == 0


# def test_representacao_agregacao():
#     assert dger.representacao_agregacao == 1


# def test_matriz_correlacao_espacial():
#     assert dger.matriz_correlacao_espacial == 1


# def test_desconsidera_convergencia_estatistica():
#     assert dger.desconsidera_convergencia_estatistica == 1


# def test_momento_reamostragem():
#     assert dger.momento_reamostragem == 1


# def test_mantem_arquivos_energias():
#     assert dger.mantem_arquivos_energias == 0


# def test_inicio_teste_convergencia():
#     assert dger.inicio_teste_convergencia == 1


# def test_sazonaliza_vmint():
#     assert dger.sazonaliza_vmint == 0


# def test_sazonaliza_vmaxt():
#     assert dger.sazonaliza_vmaxt == 0


# def test_sazonaliza_vminp():
#     assert dger.sazonaliza_vminp == 0


# def test_sazonaliza_cfuga_cmont():
#     assert dger.sazonaliza_cfuga_cmont == 0


# def test_restricoes_emissao_gee():
#     assert dger.restricoes_emissao_gee == 0


# def test_afluencia_anual_parp():
#     assert dger.afluencia_anual_parp == [3, 0]


# def test_restricoes_fornecimento_gas():
#     assert dger.restricoes_fornecimento_gas == 0


# def test_mem_calculo_cortes():
#     assert dger.memoria_calculo_cortes == 0


# def test_geracao_eolica():
#     assert dger.geracao_eolica == [1, 0.0063]


# def test_compensacao_correlacao_cruzada():
#     assert dger.compensacao_correlacao_cruzada == 1


# def test_escrita_e_leitura():
#     dger.escreve_arquivo("tests/_saidas")
#     dger2 = DGer.le_arquivo("tests/_saidas")
#     assert dger == dger2


# def test_eq_dger():
#     dger2 = DGer.le_arquivo("tests/_arquivos")
#     assert dger == dger2


# def test_neq_dger():
#     dger2 = DGer.le_arquivo("tests/_arquivos")
#     dger2.delta_zsup = -10.0
#     assert dger != dger2
