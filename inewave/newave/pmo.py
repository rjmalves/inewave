# Imports do próprio módulo
from inewave._utils.leitura import Leitura
from inewave.config import MAX_ANOS_ESTUDO, MAX_ITERS
from inewave.config import NUM_VARIAVEIS_CUSTO_PMO, REES
from inewave.config import MESES, SUBMERCADOS
from .modelos.dger import DGer
from .modelos.dger import EnumImpressaoOperacao
from .modelos.dger import EnumImpressaoConvergencia
from .modelos.dger import EnumCorrecaoEnergiaDesvio
from .modelos.dger import EnumRepresentacaoSubmotorizacao
from .modelos.dger import EnumTipoReamostragem
from .modelos.dger import EnumRepresentanteAgregacao
from .modelos.dger import EnumMatrizCorrelacaoEspacial
from .modelos.dger import EnumMomentoReamostragem
from .modelos.dger import EnumInicioTesteConvergencia
from .modelos.dger import EnumSazonaliza
from .modelos.pmo import EnergiaFioLiquidaREEPMO
from .modelos.pmo import ConfiguracoesExpansaoPMO
from .modelos.pmo import RetasPerdasEngolimentoREEPMO
from .modelos.pmo import EnergiasAfluentesPMO
from .modelos.pmo import ConvergenciaPMO
from .modelos.pmo import RiscoDeficitENSPMO
from .modelos.pmo import CustoOperacaoPMO
from .modelos.pmo import PMO
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from traceback import print_exc
from typing import IO, List, Tuple


class LeituraPMO(Leitura):
    """
    Realiza a leitura do arquivo pmo.dat
    existente em um diretório de saídas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo pmo.dat, construindo
    um objeto `PMO` cujas informações são as mesmas do pmo.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `pmo`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraPMO(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> pmo = leitor.pmo

    """
    str_dados_pmo = " DATA : "
    str_inicio_dger = "  DADOS GERAIS"
    str_inicio_converg = "    ITER               LIM.INF.        "
    str_inicio_risco = " ANO  RISCO   EENS  RISCO"
    str_inicio_custo_series = "                 CUSTO DE OPERACAO DAS"
    str_inicio_valor_esperado = "                 VALOR ESPERADO PARA PERI"
    str_inicio_custo_referenciado = "                     CUSTO OPERACAO R"
    str_inicio_efio_liquida = '***ENERGIA FIO D"AGUA LIQUIDA***'
    str_inicio_configs_expansao = "CONFIGURACOES POR QUALQUER MODIFICACAO"
    str_fim_dger = "CEPEL"
    str_fim_efio_liquida = "MODELO ESTRATEGICO DE GERACAO"
    str_fim_pmo = "DETECTADO NO CALCULO DA SIMULACAO FINAL"

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # PMO default, depois é substituído
        self.pmo = PMO(0,
                       0,
                       "",
                       DGer.dger_padrao(),
                       EnergiaFioLiquidaREEPMO(np.array([])),
                       ConfiguracoesExpansaoPMO(np.array([])),
                       RetasPerdasEngolimentoREEPMO(np.array([])),
                       EnergiasAfluentesPMO(),
                       EnergiasAfluentesPMO(),
                       EnergiasAfluentesPMO(),
                       {},
                       ConvergenciaPMO(np.array([])),
                       RiscoDeficitENSPMO([], np.array([])),
                       CustoOperacaoPMO(np.array([])),
                       CustoOperacaoPMO(np.array([])),
                       CustoOperacaoPMO(np.array([])))

    def le_arquivo(self) -> PMO:
        """
        Faz a leitura do arquivo `pmo.dat`.
        """
        try:
            caminho = os.path.join(self.diretorio, "pmo.dat")
            with open(caminho, "r") as arq:
                self.pmo = self._le_pmo(arq)
                return self.pmo
        except Exception:
            print_exc()
            return self.pmo

    def _le_pmo(self, arq: IO) -> PMO:
        """
        Faz a leitura do arquivo pmo.dat.
        """
        achou_dados_pmo = False
        leu_dados_pmo = False
        achou_dger = False
        achou_efio_liquida = False
        achou_configs_exp = False
        achou_convergencia = False
        achou_risco_ens = False
        achou_custo_series = False
        achou_valor_esperado = False
        achou_custo_refer = False
        linha = ""
        # Variáveis para armazenar os componentes do PMO, que será
        # construído quando acabar a leitura
        ano_pmo = 0
        mes_pmo = 0
        versao_newave = ""
        dger = DGer.dger_padrao()
        energia_liq = EnergiaFioLiquidaREEPMO(np.array([]))
        configs_exp = ConfiguracoesExpansaoPMO(np.array([]))
        retas_perdas = RetasPerdasEngolimentoREEPMO(np.array([]))
        convergencia = ConvergenciaPMO(np.array([]))
        risco_ens = RiscoDeficitENSPMO([], np.array([]))
        custo_series = CustoOperacaoPMO(np.array([]))
        valor_esp = CustoOperacaoPMO(np.array([]))
        custo_ref = CustoOperacaoPMO(np.array([]))
        while True:
            # Decide se lê uma linha nova ou usa a última lida
            linha = self._le_linha_com_backup(arq)
            if len(linha) == 0 or self._fim_arquivo(linha):
                self.pmo = PMO(ano_pmo,
                               mes_pmo,
                               versao_newave,
                               dger,
                               energia_liq,
                               configs_exp,
                               retas_perdas,
                               EnergiasAfluentesPMO(),
                               EnergiasAfluentesPMO(),
                               EnergiasAfluentesPMO(),
                               {},
                               convergencia,
                               risco_ens,
                               custo_series,
                               valor_esp,
                               custo_ref)
                break
            # Condição para iniciar uma leitura de dados
            if not achou_dados_pmo and not leu_dados_pmo:
                achou = LeituraPMO.str_dados_pmo in linha
                achou_dados_pmo = achou
            if not achou_dger:
                achou = LeituraPMO.str_inicio_dger in linha
                achou_dger = achou
            if not achou_efio_liquida:
                achou = LeituraPMO.str_inicio_efio_liquida in linha
                achou_efio_liquida = achou
            if not achou_configs_exp:
                achou = LeituraPMO.str_inicio_configs_expansao in linha
                achou_configs_exp = achou
            if not achou_convergencia:
                achou = LeituraPMO.str_inicio_converg in linha
                achou_convergencia = achou
            if not achou_risco_ens:
                achou = LeituraPMO.str_inicio_risco in linha
                achou_risco_ens = achou
            if not achou_custo_series:
                achou = LeituraPMO.str_inicio_custo_series in linha
                achou_custo_series = achou
            if not achou_valor_esperado:
                achou = LeituraPMO.str_inicio_valor_esperado in linha
                achou_valor_esperado = achou
            if not achou_custo_refer:
                achou = LeituraPMO.str_inicio_custo_referenciado in linha
                achou_custo_refer = achou
            # Quando achar, le cada parte adequadamente
            if achou_dados_pmo:
                ano_pmo, mes_pmo, versao_newave = self._le_dados_pmo(linha)
                achou_dados_pmo = False
                leu_dados_pmo = True
            if achou_dger:
                dger = self._le_dger(arq)
                achou_dger = False
            if achou_efio_liquida:
                energia_liq, retas_perdas = self._le_efio_liquida(arq)
                achou_efio_liquida = False
            if achou_configs_exp:
                configs_exp = self._le_configs_expansao(arq)
                achou_configs_exp = False
            if achou_convergencia:
                convergencia = self._le_convergencia(arq)
                achou_convergencia = False
            if achou_risco_ens:
                risco_ens = self._le_risco_ens(arq)
                achou_risco_ens = False
            if achou_custo_series:
                custo_series = self._le_tabela_custo(arq)
                achou_custo_series = False
            if achou_valor_esperado:
                valor_esp = self._le_tabela_custo(arq)
                achou_valor_esperado = False
            if achou_custo_refer:
                custo_ref = self._le_tabela_custo(arq)
                achou_custo_refer = False

        return self.pmo

    def _le_dados_pmo(self, linha: str) -> Tuple[int, int, str]:
        """
        Lê a linha com dados do PMO em questão e retorna dados
        sobre o mês e ano de estudo e a versão do NEWAVE usada.
        """
        # Procura o mês do PMO
        mes_pmo = 0
        for i, m in enumerate(MESES):
            if m in linha:
                mes_pmo = i + 1
                break
        # Quebra a linha no nome do mês
        ano_pmo = int(linha.split(MESES[mes_pmo-1])[1][3:7])
        # Encontra a versao do NW
        versao_newave = linha.split("Versao")[1].strip()
        return ano_pmo, mes_pmo, versao_newave

    def _le_dger(self, arq: IO) -> DGer:
        """
        Lê o eco dos dados gerais de entrada fornecidos ao caso.
        """
        dger = DGer.dger_padrao()
        ci = 57

        def le_parametro(linha: str):
            aux = linha[5:54]
            param = linha[ci:].strip()
            if "DURACAO DE CADA PERIODO" in aux:
                dger.duracao_estagio_op = int(param)
            elif "NUMERO DE ANOS DO HORIZONTE DE" in aux:
                dger.num_anos_estudo = int(param)
            elif "MES INICIAL DO PERIODO DE PRE" in aux:
                dger.mes_inicio_pre_estudo = int(param)
            elif "MES INICIAL DO PERIODO DE EST" in aux:
                dger.mes_inicio_estudo = int(param)
            elif "ANO INICIAL DO PERIODO DE EST" in aux:
                dger.ano_inicio_estudo = int(param)
            elif "NUMERO DE ANOS QUE PRECEDEM O HOR" in aux:
                dger.num_anos_pre_estudo = int(param)
            elif "NUMERO DE ANOS QUE SUCEDEM O HOR" in aux:
                dger.num_anos_pos_estudo = int(param)
            elif "NUMERO DE ANOS DO POS NA SIMULACAO" in aux:
                dger.num_anos_pos_sim_final = int(param)
            elif "IMPRIME DADOS DAS USINAS " in aux:
                p = param
                dger.imprime_dados_usinas = (True if p == "SIM"
                                             else False)
            elif "IMPRIME DADOS DE MERCADO" in aux:
                p = param
                dger.imprime_dados_mercados = (True if p == "SIM"
                                               else False)
            elif "IMPRIME DADOS DE ENERGIAS" in aux:
                p = param
                dger.imprime_dados_energias = (True if p == "SIM"
                                               else False)
            elif "IMPRIME PARAMETROS DO MODELO DE ENERGIA" in aux:
                p = param
                dger.imprime_dados_modelo = (True if p == "SIM"
                                             else False)
            elif "IMPRIME PARAMETROS DO RESERVATORIO EQUIV" in aux:
                p = param
                dger.imprime_dados_rees = (True if p == "SIM"
                                           else False)
            elif "NUMERO MAXIMO DE ITERACOES" in aux:
                dger.max_iteracoes = int(param)
            elif "NUMERO DE SIMULACOES" in aux:
                dger.num_sim_forward = int(param)
            elif "NUMERO DE ABERTURAS" in aux:
                dger.num_aberturas = int(param)
            elif "TOTAL DE SERIES SIMULADAS GRAVADAS" in aux:
                dger.num_series_sinteticas = int(param)
            elif "ORDEM MAXIMA DO MODELO DE ENERGI" in aux:
                dger.ordem_maxima_parp = int(param)
            elif "ANO INICIAL DO HISTORICO DE" in aux:
                dger.ano_inicial_vaz_historicas = int(param)
            elif "CALCULA VOLUME INICIAL" in aux:
                p = param
                dger.calcula_vol_inicial = (True if p == "SIM"
                                            else False)
            elif "TOLERANCIA PARA CONVERGENCIA" in aux:
                dger.tolerancia = float(param)
            elif "TAXA DE DESCONTO ANUAL (%)" in aux:
                dger.taxa_de_desconto = float(param)
            elif "IMPRIME DETALHAMENTO DA OPERACAO" in aux:
                val = (0 if param == "NAO" else 1)
                impr_op = EnumImpressaoOperacao.infere_valor(val)
                dger.impressao_operacao = impr_op
            elif "IMPRIME RESULTADOS DA CONVERGENCIA" in aux:
                val = (0 if param == "NAO" else 1)
                impr_c = EnumImpressaoConvergencia.infere_valor(val)
                dger.impressao_convergencia = impr_c
            elif "NUMERO MINIMO DE ITERACOES" in aux:
                dger.min_interacoes = int(param)
            elif "ADOCAO DE RACIONAMENTO PREVENTIVO" in aux:
                p = param
                dger.racionamento_preventivo = (True if p == "SIM"
                                                else False)
            elif "LIDA DO ARQUIVO DE MANUTENCOES" in aux:
                dger.numero_anos_manutencao_UTEs = int(param)
            elif "CONSIDERA PERDAS NA REDE DE TRANSMISSAO" in aux:
                p = param
                dger.perdas_transmissao = (True if p == "SIM"
                                           else False)
            elif "CONSIDERA OUTROS USOS DA AGUA" in aux:
                p = param
                dger.considera_desvio_dagua = (True if p == "SIM"
                                               else False)
            elif "OUTROS USOS DA AGUA VARIAVEL COM A ENERGIA" in aux:
                val = (0 if param == "NAO" else 1)
                des = EnumCorrecaoEnergiaDesvio.infere_valor(val)
                dger.correcao_energia_desvio = des
            elif "CONSIDERA CURVA GUIA DE SEGURANCA/VMINP" in aux:
                p = param
                dger.considera_curva_aversao = (True if p == "SIM"
                                                else False)
            elif "AGRUPAMENTO LIVRE" in aux:
                p = param
                dger.agrupamento_livre_interc = (True
                                                 if p == "SIM"
                                                 else False)
            elif "CONSIDERA EQUALIZACAO DE PENALIDADES DE" in aux:
                p = param
                dger.equaliza_penalidades_interc = (True
                                                    if p == "SIM"
                                                    else False)
            elif "CONSIDERA SUBMOTORIZACAO SAZONAL" in aux:
                val = (0 if param == "NAO" else
                       2 if "USINA" in param else 1)
                sm = EnumRepresentacaoSubmotorizacao.infere_valor(val)
                dger.representa_submotor = sm
            elif "CONSIDERA ORDENACAO AUTOMATICA REEs" in aux:
                p = linha[66:].strip()
                dger.ordenacao_automatica_subsist = (True
                                                     if p == "SIM"
                                                     else False)
            elif "CONSIDERA CARGAS ADICIONAIS" in aux:
                p = param
                dger.considera_cargas_adicionais = (True
                                                    if p == "SIM"
                                                    else False)
            elif "DELTA DE ZSUP" in aux:
                dger.delta_zsup = float(param[:-1])
            elif "DELTA DE ZINF" in aux:
                dger.delta_zinf = float(param[:-1])
            elif "NUMERO DE DELTAS DE ZINF CONSECUTIVOS" in aux:
                dger.deltas_consecutivos = int(param)
            elif "CONSIDERA ANTECIPACAO DE GERACAO" in aux:
                p = param
                dger.considera_despacho_gnl = (True
                                               if p == "SIM"
                                               else False)
            elif "ANTECIPACAO DE GERACAO TERMOELETRICA" in aux:
                p = param
                dger.modifica_auto_despacho_gnl = (True
                                                   if p == "SIM"
                                                   else False)
            elif "CONSIDERA GERACAO HIDRAULICA MINIMA" in aux:
                p = param
                dger.considera_ghmin = (True
                                        if p == "SIM"
                                        else False)
            elif "CONSIDERA GERENCIAMENTO EXTERNO DE PROCESSOS" in aux:
                p = param
                dger.gerenciador_externo = (True if p == "SIM"
                                            else False)
            elif "CONSIDERA COMUNICACAO EM DOIS NIVEIS" in aux:
                p = param
                dger.comunicacao_dois_niveis = (True if p == "SIM"
                                                else False)
            elif "CONSIDERA ARMAZENAMENTO LOCAL DE ARQUIVOS" in aux:
                p = param
                dger.armazenamento_local_temp = (True if p == "SIM"
                                                 else False)
            elif "CONSIDERA ALOCACAO DE ENERGIA EM MEMORIA" in aux:
                p = param
                dger.aloca_memoria_enas = (True if p == "SIM"
                                           else False)
            elif "CONSIDERA ALOCACAO DE CORTES EM MEMORIA" in aux:
                p = param
                dger.aloca_memoria_cortes = (True if p == "SIM"
                                             else False)
            elif "CONSIDERA SUPERFICIE DE AVERSAO A RISCO (SAR)" in aux:
                p = param
                dger.sar = (True if p == "SIM"
                            else False)
            elif "CONSIDERA MECANISMO DE AVERSAO AO RISCO (CVAR)" in aux:
                p = param
                dger.cvar = (True if "SIM" in p
                             else False)
            elif "DESCONSIDERA VAZAO MINIMA" in aux:
                p = param
                dger.desconsidera_vazao_minima = (True if p == "SIM"
                                                  else False)
            elif "CONSIDERA RESTRICOES ELETRICAS NO REE" in aux:
                p = param
                dger.considera_restricoes_elet = (True if p == "SIM"
                                                  else False)
            elif "CONSIDERA SELECAO DE CORTES DE BENDERS" in aux:
                p = param
                dger.selecao_cortes_benders = (True if p == "SIM"
                                               else False)
            elif "CONSIDERA JANELA DE CORTES DE BENDERS" in aux:
                p = param
                dger.janela_selecao_cortes = (True if p == "SIM"
                                              else False)
            elif "CONSIDERA REAMOSTRAGEM DE CENARIOS" in aux:
                p = param
                dger.reamostragem = (True if p == "SIM"
                                     else False)
            elif "PASSO DA REAMOSTRAGEM:" in aux:
                p = linha[33:37].strip()
                dger.passo_reamostragem = int(p)
            elif "TIPO DA REAMOSTRAGEM" in aux:
                t = (0 if "SORTEIA NOVOS RUIDOS" in param else 1)
                tipo_reamos = EnumTipoReamostragem.infere_valor(t)
                dger.tipo_reamostragem = tipo_reamos
            elif "CONSIDERA ZINF CALCULADO NO NO ZERO" in aux:
                p = param
                dger.considera_convergencia_no0 = (True
                                                   if p == "SIM"
                                                   else False)
            elif "REALIZA ACESSO A FCF PARA CONVERGENCIA" in aux:
                p = param
                dger.consulta_fcf = (True
                                     if p == "SIM"
                                     else False)
            elif "CENARIOS DE ENERGIA:" in aux:
                p = linha[36:]
                dger.impressao_ena = (True
                                      if p == "SIM"
                                      else False)
            elif "CORTES ATIVOS:" in aux:
                p = linha[36:]
                dger.impressao_cortes_ativos = (True
                                                if p == "SIM"
                                                else False)
            elif "REPRESENTANTE NO PROCESSO DE AGREGACAO" in aux:
                p = linha[45:]
                t = (1 if "CENTROIDE" in p else 0)
                ra = EnumRepresentanteAgregacao.infere_valor(t)
                dger.representante_agregacao = ra
            elif "MATRIZ DE CORRELACAO ESPACIAL CONSIDERADA" in aux:
                p = linha[48:]
                t = (1 if "MENSAL" in p else 0)
                mc = EnumMatrizCorrelacaoEspacial.infere_valor(t)
                dger.matriz_corr_espacial = mc
            elif "DESCONSIDERA CRITERIO DE CONV. ESTATISTICO" in aux:
                p = param
                dger.desconsidera_converg_estatist = (True
                                                      if p == "SIM"
                                                      else False)
            elif "MOMENTO DE REAMOSTRAGEM" in aux:
                p = linha[30:]
                t = (1 if "FORWARD" in p else 0)
                mr = EnumMomentoReamostragem.infere_valor(t)
                dger.momento_reamostragem = mr
            elif "MANTEM OS ARQUIVOS DE ENERGIAS APOS EXECUCAO" in aux:
                p = linha[51:].strip()
                dger.mantem_arquivos_ena = (True
                                            if p == "SIM"
                                            else False)
            elif "INICIO TESTE CONVERG." in aux:
                t = (1 if int(param) > 1 else 0)
                tc = EnumInicioTesteConvergencia.infere_valor(t)
                dger.inicio_teste_convergencia = tc
            elif "VOLUME MINIMO COM DATA SAZONAL NOS PERIODOS" in aux:
                p = param
                t = (1 if "SIM" in p else 0)
                sv = EnumSazonaliza.infere_valor(t)
                dger.sazonaliza_vmint = sv
            elif "VOLUME MAXIMO COM DATA SAZONAL NOS PERIODOS" in aux:
                p = param
                t = (1 if "SIM" in p else 0)
                sv = EnumSazonaliza.infere_valor(t)
                dger.sazonaliza_vmaxt = sv
            elif "VOLUME MAXIMO PENAL. SAZONAL NOS PERIODOS" in aux:
                p = param
                t = (1 if "SIM" in p else 0)
                sv = EnumSazonaliza.infere_valor(t)
                dger.sazonaliza_vminp = sv
            elif "CFUGA E CMONT SAZONAIS NOS PERIODOS" in aux:
                p = linha[53:].strip()
                t = (1 if "SIM" in p else 0)
                sv = EnumSazonaliza.infere_valor(t)
                dger.sazonaliza_cfuga_cmont = sv
            elif "CONSIDERA RESTRICOES DE LIMITES DE EMISSAO" in aux:
                p = param
                dger.restricoes_gee = (True
                                       if p == "SIM"
                                       else False)
            elif "CONSIDERA AFLUENCIA ANUAL NOS MODELOS" in aux:
                p = param
                af = (True
                      if p == "SIM"
                      else False)
                af_existente = dger.afluencia_anual_parp[1]
                dger.afluencia_anual_parp = (af, af_existente)
            elif "CONSIDERA VERIFICACAO AUTOMATICA DA ORDEM DO" in aux:
                p = linha[63:].strip()
                af = (True
                      if p == "SIM"
                      else False)
                af_existente = dger.afluencia_anual_parp[0]
                dger.afluencia_anual_parp = (af_existente, af)
            elif "CONSIDERACAO DA INCERTEZA NA GERACAO EOLICA" in aux:
                p = param
                dger.incerteza_ger_eolica = (True
                                             if p == "SIM"
                                             else False)
            elif "CONSIDERACAO DA INCERTEZA NA GERACAO SOLAR " in aux:
                p = param
                dger.incerteza_ger_solar = (True
                                            if p == "SIM"
                                            else False)
            elif "CONSIDERA RESTRICOES DE FORNECIMENTO DE GAS" in aux:
                p = param
                dger.restricoes_fornecimento_gas = (True
                                                    if p == "SIM"
                                                    else False)

        while True:
            linha = self._le_linha_com_backup(arq)
            # Confere se a parte do DGer já acabou
            if LeituraPMO.str_fim_dger in linha:
                break
            # Senão, lê mais um parâmetro
            le_parametro(linha)
        return dger

    def _le_efio_liquida(self,
                         arq: IO
                         ) -> Tuple[EnergiaFioLiquidaREEPMO,
                                    RetasPerdasEngolimentoREEPMO]:
        """
        Lê as tabelas de energia fio d'água líquida e as retas de
        perdas de energia fio d'água por REE.
        """
        # Inicia as variáveis que serão retornadas, com as tabelas
        # de energia fio d'água líquidas e as retas de perdas.
        tabela_energias: np.ndarray = np.array([])
        tabela_perdas: np.ndarray = np.array([])
        montou_tabela_energias = False
        montou_tabela_perdas = False
        achou_ree_energias = False
        achou_inicio_ree_perdas = False
        achou_ree_perdas = False
        n_rees = len(REES)
        rees_lidos = 0
        while True:
            # Confere se a leitura não acabou
            linha = self._le_linha_com_backup(arq)
            if rees_lidos == n_rees:
                return (EnergiaFioLiquidaREEPMO(tabela_energias),
                        RetasPerdasEngolimentoREEPMO(tabela_perdas))
            # Confere se já achou a tabela de energia da próxima REE
            if 'CONFIGURACAO DO PERIODO' in linha:
                achou_ree_energias = True
            # Confere se já achou a tabela de retas da próxima REE
            if "PERDAS POR ENGOLIMENTO MAXIMO" in linha:
                achou_inicio_ree_perdas = True
            if "REE:" in linha and achou_inicio_ree_perdas:
                # Salta uma linha para ter informação da REE
                achou_ree_perdas = True
            if achou_ree_energias:
                # Infere a REE em questão
                ree = REES.index(linha[6:18].strip()) + 1
                if not montou_tabela_energias:
                    # Se não leu nenhuma tabela ainda, usa a da primeira REE
                    # como exemplo para inicializar a variável completa
                    tabela_exemplo = self._le_tabela_efio(arq)
                    dims = tabela_exemplo.shape
                    tabela_energias = np.zeros((len(REES),
                                                dims[0],
                                                dims[1]))
                    tabela_energias[ree-1, :, :] = tabela_exemplo
                    montou_tabela_energias = True
                else:
                    tabela_energias[ree-1, :, :] = self._le_tabela_efio(arq)
                achou_ree_energias = False
            if achou_ree_perdas:
                ree = REES.index(linha[6:18].strip()) + 1
                if not montou_tabela_perdas:
                    # Se não leu nenhuma tabela ainda, usa a da primeira REE
                    # como exemplo para inicializar a variável completa
                    tabela_exemplo = self._le_tabela_perdas(arq)
                    dims = tabela_exemplo.shape
                    tabela_perdas = np.zeros((len(REES),
                                              dims[0],
                                              dims[1]))
                    tabela_perdas[ree-1, :, :] = tabela_exemplo
                    montou_tabela_perdas = True
                else:
                    tabela_perdas[ree-1, :, :] = self._le_tabela_perdas(arq)
                achou_ree_perdas = False
                rees_lidos += 1

    def _le_tabela_efio(self, arq: IO) -> np.ndarray:
        """
        Lê as informações de uma tabela de energias fio d'água líquidas.
        """
        tabela: List[List[float]] = []
        # Pula a linha do cabeçalho dos meses
        self._le_linha_com_backup(arq)
        n_meses = len(MESES)
        ci_ano = 5
        cf_ano = 10
        while True:
            linha = self._le_linha_com_backup(arq)
            # Confere se a tabela não acabou
            if len(linha) <= 1:
                return np.array(tabela)
            ci = 11
            nc = 7
            # Armazena as informações de uma linha
            dados_linha: List[float] = []
            dados_linha.append(float(linha[ci_ano:cf_ano]))
            for i in range(n_meses):
                cf = ci + nc
                dados_linha.append(float(linha[ci:cf]))
                ci = cf + 2
            tabela.append(dados_linha)

    def _le_configs_expansao(self, arq: IO) -> ConfiguracoesExpansaoPMO:
        """
        Lê as informações da tabela de configurações por período
        de acordo com a expansão do sistema.
        """
        n_meses = len(MESES)
        tabela = np.zeros((MAX_ANOS_ESTUDO, n_meses + 1),
                          dtype=np.int64)
        # Pula 5 linhas
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        i = 0
        while True:
            linha = self._le_linha_com_backup(arq)
            # Confere se a tabela não acabou
            if len(linha) <= 3:
                return ConfiguracoesExpansaoPMO(tabela[:i, :])
            ci = 5
            nc = 5
            # Armazena as informações de uma linha
            for j in range(n_meses + 1):
                cf = ci + nc
                tabela[i, j] = float(linha[ci:cf].strip())
                ci = cf + 1
            i += 1

    def _le_tabela_perdas(self, arq: IO) -> np.ndarray:
        """
        Lê as informações de uma tabela de retas das perdas de
        energia fio d'água.
        """
        tabela: List[List[float]] = []
        # Pula 4 linhas - entre a identificação da REE e o
        # início da tabela
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        while True:
            linha = self._le_linha_com_backup(arq)
            # Confere se a tabela não acabou
            if len(linha) <= 1:
                return np.array(tabela)
            ci = 1
            nc = 12
            # Armazena as informações de uma linha
            dados_linha: List[float] = []
            for i in range(3):
                cf = ci + nc
                dados_linha.append(float(linha[ci:cf].strip()))
                ci = cf + 1
            tabela.append(dados_linha)

    def _le_convergencia(self, arq: IO) -> ConvergenciaPMO:
        """
        Lê as linhas que formam a tabela do relatório de convergência
        da execução do NEWAVE.
        """
        # Salta duas linhas depois de identificar o início do relatório
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        # Inicia as variáveis
        tabela = np.zeros((MAX_ITERS, 6))
        i = 0
        while True:
            linha = self._le_linha_com_backup(arq)
            # Confere se já acabou
            if len(linha) < 2:
                return ConvergenciaPMO(tabela[:i, :])
            # Senão, confere se a linha não tem dados relevantes
            if not linha[4:8].strip().isnumeric():
                continue
            # Lê a linha normalmente
            it = int(linha[4:8])
            liminf = float(linha[9:31])
            zinf = float(linha[32:54])
            limsup = float(linha[55:77])
            zsup = float(linha[78:100])
            # Converte o tempo, se for informado nessa linha
            # Senão, pega da linha anterior
            str_tempo = linha[153:169]
            tempo = 0.0
            if "min" in str_tempo:
                str_horas = str_tempo.split('h')[0]
                str_min = str_tempo.split('h')[1].split('min')[0]
                str_seg = str_tempo.split('min')[1].split('s')[0]
                tempo = (float(str_seg) +
                         60 * float(str_min) +
                         3600 * float(str_horas))
            else:
                tempo = tabela[i - 1, -1]
            # Armazena na linha da tabela
            tabela[i, :] = np.array([it, liminf, zinf, limsup, zsup, tempo])
            i += 1

    def _le_risco_ens(self, arq: IO) -> RiscoDeficitENSPMO:
        """
        Lê as linhas que formam a tabela de RISCO e ENS por ano
        de estudo e subsistema.
        """
        # Salta duas linhas após a string de início ser identificada
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        # Inicializa as variáveis de interesse
        anos_estudo: List[int] = []
        linhas_tabela = MAX_ANOS_ESTUDO
        colunas_tabela = 2 * len(SUBMERCADOS)
        tabela = np.zeros((linhas_tabela, colunas_tabela))
        campos_colunas = [5, 7] * len(SUBMERCADOS)
        # Lê a tabela
        i = 0
        while True:
            linha = self._le_linha_com_backup(arq)
            # Confere se a tabela já acabou
            if len(linha) <= 1:
                # Constroi o objeto e retorna
                return RiscoDeficitENSPMO(anos_estudo, tabela[:i, :])
            anos_estudo.append(int(linha[1:5]))
            ci = 7
            for j in range(colunas_tabela):
                cf = ci + campos_colunas[j]
                tabela[i, j] = float(linha[ci:cf])
                ci = cf + 1
            i += 1

    def _le_tabela_custo(self, arq: IO) -> CustoOperacaoPMO:
        """
        Lê as linhas que formam uma das tabelas de composição
        do valor total de operação do pmo.dat.
        """
        inicio_tabela = "PARCELA           V.ESPERADO"
        iniciou = False
        # Procura o cabeçalho da tabela
        linha = ""
        while not iniciou:
            linha = self._le_linha_com_backup(arq)
            iniciou = inicio_tabela in linha
        # Pula uma linha
        self._le_linha_com_backup(arq)
        # Cria a variável para armazenar a tabela
        tabela = np.zeros((NUM_VARIAVEIS_CUSTO_PMO, 3))
        # Lê cada uma das variáveis
        abs_i = 32
        abs_f = 45
        perc_i = 46
        dp_i = 47
        dp_f = 59
        perc_i = 60
        perc_f = 67
        for i in range(NUM_VARIAVEIS_CUSTO_PMO):
            linha = self._le_linha_com_backup(arq)
            tabela[i, 0] = float(linha[abs_i:abs_f])
            tabela[i, 1] = float(linha[dp_i:dp_f])
            tabela[i, 2] = float(linha[perc_i:perc_f])
        return CustoOperacaoPMO(tabela)

    def _fim_arquivo(self, linha: str) -> bool:
        return LeituraPMO.str_fim_pmo in linha
