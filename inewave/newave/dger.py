# Imports do próprio módulo
from inewave._utils.leitura import Leitura
from .modelos.dger import DGer
from .modelos.dger import EnumDuracaoPatamar
from .modelos.dger import EnumCorrecaoEnergiaDesvio
from .modelos.dger import EnumInicioTesteConvergencia
from .modelos.dger import EnumMatrizCorrelacaoEspacial
from .modelos.dger import EnumMomentoReamostragem
from .modelos.dger import EnumRepresentacaoSubmotorizacao
from .modelos.dger import EnumRepresentanteAgregacao
from .modelos.dger import EnumTendenciaHidrologica
from .modelos.dger import EnumTipoExecucao
from .modelos.dger import EnumTipoGeracaoENAs
from .modelos.dger import EnumTipoReamostragem
from .modelos.dger import EnumTipoSimulacaoFinal
# Imports de módulos externos
import os
from traceback import print_exc


class LeituraDGer(Leitura):
    """
    Classe para realizar a leitura do arquivo dger.dat
    existente em um diretório de entradas do NEWAVE.
    """
    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # DGer default, depois é substituído
        self.dger = DGer.dger_padrao()

    def le_arquivo(self) -> DGer:
        """
        Realiza a leitura do arquivo dger.dat.
        """
        try:
            caminho = os.path.join(self.diretorio, "dger.dat")
            with open(caminho, "r") as arq:
                # Lê o nome do estudo e restringe até a coluna 80
                nome = self._le_linha_com_backup(arq)
                self.dger.nome_estudo = nome[:min([79, len(nome)])]
                # Lê os demais parâmetros
                ci = 21
                cf = 25

                def le_parametro():
                    return self._le_linha_com_backup(arq)[ci:cf].strip()

                # Tipo de execução
                t = int(le_parametro())
                self.dger.tipo_execucao = EnumTipoExecucao.infere_valor(t)
                # Duração do período
                self.dger.duracao_estagio_op = int(le_parametro())
                # Num. anos do estudo
                self.dger.num_anos_estudo = int(le_parametro())
                # Mês início do pré-estudo
                self.dger.mes_inicio_pre_estudo = int(le_parametro())
                # Mês início do estudo
                self.dger.mes_inicio_estudo = int(le_parametro())
                # Ano de início do estudo
                self.dger.ano_inicio_estudo = int(le_parametro())
                # Num. anos pré-estudo
                self.dger.num_anos_pre_estudo = int(le_parametro())
                # Num. anos pós estudo
                self.dger.num_anos_pos_estudo = int(le_parametro())
                # Num. anos pós estudo na sim final
                self.dger.num_anos_pos_sim_final = int(le_parametro())
                # Impressão de dados das usinas
                p = le_parametro()
                self.dger.imprime_dados_usinas = (True if p == "1"
                                                  else False)
                # Impressão de dados dos mercados
                p = le_parametro()
                self.dger.imprime_dados_mercados = (True if p == "1"
                                                    else False)
                # Impressão de dados de energias
                p = le_parametro()
                self.dger.imprime_dados_energias = (True if p == "1"
                                                    else False)
                # Impressão de dados do modelo estocástico
                p = le_parametro()
                self.dger.imprime_dados_modelo = (True if p == "1"
                                                  else False)
                # Impressão de dados das REEs
                p = le_parametro()
                self.dger.imprime_dados_rees = (True if p == "1"
                                                else False)
                # Máximo de iterações
                self.dger.max_iteracoes = int(le_parametro())
                # Num. de forwards
                self.dger.num_sim_forward = int(le_parametro())
                # Num. de aberturas
                self.dger.num_aberturas = int(le_parametro())
                # Num. de séries sintéticas
                self.dger.num_series_sinteticas = int(le_parametro())
                # Ordem máxima do Par(P)
                self.dger.ordem_maxima_parp = int(le_parametro())
                # Ano inicial do histórico de afluências e tamanho
                p = self._le_linha_com_backup(arq)
                self.dger.ano_inicial_vaz_historicas = int(p[ci:cf].strip())
                self.dger.tamanho_arq_vaz_historicas = int(p[28])
                # Cálculo da energia armazenada dos volumes iniciais
                p = le_parametro()
                self.dger.calcula_vol_inicial = (True if p == "1"
                                                 else False)
                # Ignora a linha de cabeçalho dos volumes iniciais
                self._le_linha_com_backup(arq)
                # Lê os volumes de cada subsistema
                p = self._le_linha_com_backup(arq)
                cisub = 22
                n_col_sub = 5
                for i in range(4):
                    cfsub = cisub + n_col_sub
                    v = float(p[cisub:cfsub])
                    self.dger.vol_inicial_subsistema[i] = v
                    cisub = cfsub + 2
                # Tolerância
                self.dger.tolerancia = float(le_parametro())
                # Taxa de desconto
                self.dger.taxa_de_desconto = float(le_parametro())
                # Tipo de simulação final
                t = int(le_parametro())
                tipo = EnumTipoSimulacaoFinal.infere_valor(t)
                self.dger.tipo_simulacao_final = tipo
                # Opções de impressão
                p = le_parametro()
                self.dger.impressao_operacao = (True if p == "1"
                                                else False)
                p = le_parametro()
                self.dger.impressao_convergencia = (True if p == "1"
                                                    else False)
                # Intervalo de gravação
                self.dger.intervalo_gravacao_relatorio = int(le_parametro())
                # Mínimo de iterações
                self.dger.min_interacoes = int(le_parametro())
                # Racionamento preventivo
                p = le_parametro()
                self.dger.racionamento_preventivo = (True if p == "1"
                                                     else False)
                # Número de anos de manutenção da UTEs
                self.dger.numero_anos_manutencao_UTEs = int(le_parametro())
                # Tendência hidrológica
                t = int(le_parametro())
                tendencia = EnumTendenciaHidrologica.infere_valor(t)
                self.dger.tendencia_hidrologica = tendencia
                # Itaipu
                p = le_parametro()
                self.dger.restricoes_itaipu = (True if p == "1"
                                               else False)
                # Bidding
                p = le_parametro()
                self.dger.bidding_demanda = (True if p == "1"
                                             else False)
                # Perdas da transmissão
                p = le_parametro()
                self.dger.perdas_transmissao = (True if p == "1"
                                                else False)
                # El Niño
                p = le_parametro()
                self.dger.el_nino = (True if p == "1"
                                     else False)
                # ENSO
                p = le_parametro()
                self.dger.enso = (True if p == "1"
                                  else False)
                # Duração por patamar
                t = int(le_parametro())
                self.dger.duracao_patamar = EnumDuracaoPatamar.infere_valor(t)
                # Outros usos da água
                p = le_parametro()
                self.dger.considera_desvio_dagua = (True if p == "1"
                                                    else False)
                # Correção da energia de desvio
                t = int(le_parametro())
                correcao = EnumCorrecaoEnergiaDesvio.infere_valor(t)
                self.dger.correcao_energia_desvio = correcao
                # Curva de aversão (VminP)
                p = le_parametro()
                self.dger.considera_curva_aversao = (True if p == "1"
                                                     else False)
                # Tipos de geração das ENAs
                t = int(le_parametro())
                tipo_geracao = EnumTipoGeracaoENAs.infere_valor(t)
                self.dger.tipo_geracao_afluencias = tipo_geracao
                # Risco de déficit
                p = self._le_linha_com_backup(arq)
                p1 = float(p[21:25].strip())
                p2 = float(p[27:31].strip())
                self.dger.profundidade_risco_deficit = (p1, p2)
                # Iteração para simulação final
                self.dger.iteracao_sim_final = int(le_parametro())
                # Agrupamento de intercâmbios
                p = le_parametro()
                self.dger.agrupamento_livre_interc = (True if p == "1"
                                                      else False)
                # Equalização de penalidades de intercâmbio
                p = le_parametro()
                self.dger.equaliza_penalidades_interc = (True if p == "1"
                                                         else False)
                # Representação da submotorização
                t = int(le_parametro())
                submot = EnumRepresentacaoSubmotorizacao.infere_valor(t)
                self.dger.representa_submotor = submot
                # Ordenação automática
                p = le_parametro()
                self.dger.ordenacao_automatica_subsist = (True if p == "1"
                                                          else False)
                # Considera cargas adicionais
                p = le_parametro()
                self.dger.considera_cargas_adicionais = (True if p == "1"
                                                         else False)
                # Variação do Zsup e Zinf
                self.dger.delta_zsup = float(le_parametro())
                self.dger.delta_zinf = float(le_parametro())
                # Núm. de deltas para convergência
                self.dger.deltas_consecutivos = int(le_parametro())
                # Despacho antecipado GNL
                p = le_parametro()
                self.dger.considera_despacho_gnl = (True if p == "1"
                                                    else False)
                # Modificação automática da Ad. Term.
                p = le_parametro()
                self.dger.modifica_auto_despacho_gnl = (True if p == "1"
                                                        else False)
                # Considera GHmin
                p = le_parametro()
                self.dger.considera_ghmin = (True if p == "1"
                                             else False)
                # Simulação final com data
                p = le_parametro()
                self.dger.sim_final_com_data = (True if p == "1"
                                                else False)
                # Gerenciador externo, comunicação em 2 níveis, ...
                p = self._le_linha_com_backup(arq)
                p1 = p[21:25].strip()
                p2 = p[26:30].strip()
                p3 = p[31:35].strip()
                p4 = p[36:40].strip()
                p5 = p[41:45].strip()
                self.dger.gerenciador_externo = (True if p1 == "1"
                                                 else False)
                self.dger.comunicacao_dois_niveis = (True if p2 == "1"
                                                     else False)
                self.dger.armazenamento_local_temp = (True if p3 == "1"
                                                      else False)
                self.dger.aloca_memoria_enas = (True if p4 == "1"
                                                else False)
                self.dger.aloca_memoria_cortes = (True if p5 == "1"
                                                  else False)
                # SAR e CVaR
                p = le_parametro()
                self.dger.sar = (True if p == "1"
                                 else False)
                p = le_parametro()
                self.dger.cvar = (True if p == "1"
                                  else False)
                # Critério de mínimo Zsup para convergência
                p = le_parametro()
                self.dger.convergencia_minimo_zsup = (True if p == "1"
                                                      else False)
                # Vazmin
                p = le_parametro()
                self.dger.considera_vazao_minima = (True if p == "1"
                                                    else False)
                # Restrições elétricas
                p = le_parametro()
                self.dger.considera_restricoes_elet = (True if p == "1"
                                                       else False)
                # Seleção de cortes
                p = le_parametro()
                self.dger.selecao_cortes_benders = (True if p == "1"
                                                    else False)
                # Janela de cortes
                p = le_parametro()
                self.dger.janela_selecao_cortes = (True if p == "1"
                                                   else False)
                # Reamostragem de cenários
                p = self._le_linha_com_backup(arq)
                reamos = p[21:25].strip()
                self.dger.reamostragem = bool(int(reamos))
                # Tipo de reamostragem
                reamos = p[26:30].strip()
                tipo_reamos = EnumTipoReamostragem.infere_valor(int(reamos))
                self.dger.tipo_reamostragem = tipo_reamos
                # Passo para reamostragem
                self.dger.passo_reamostragem = int(p[31:35])
                # Considera convergência do nó 0
                p = le_parametro()
                self.dger.considera_convergencia_no0 = (True if p == "1"
                                                        else False)
                # Consulta FCF
                p = le_parametro()
                self.dger.consulta_fcf = (True if p == "1"
                                          else False)
                # Impressão ENA
                p = le_parametro()
                self.dger.impressao_ena = bool(int(p))
                # Impressão cortes ativos
                p = le_parametro()
                self.dger.impressao_cortes_ativos = bool(int(p))
                # Representante da agregação
                p = le_parametro()
                repres = EnumRepresentanteAgregacao.infere_valor(int(p))
                self.dger.representante_agregacao = repres
                # Matriz de correlação espacial
                p = le_parametro()
                matriz = EnumMatrizCorrelacaoEspacial.infere_valor(int(p))
                self.dger.matriz_corr_espacial = matriz
                # Desconsidera convergência estatística
                p = le_parametro()
                self.dger.desconsidera_converg_estatist = bool(int(p))
                # Momento da reamostragem
                p = le_parametro()
                momento = EnumMomentoReamostragem.infere_valor(int(p))
                self.dger.momento_reamostragem = momento
                # Manter arquivos ENA
                p = le_parametro()
                self.dger.mantem_arquivos_ena = bool(int(p))
                # Início do teste de convergência
                p = le_parametro()
                inicio = EnumInicioTesteConvergencia.infere_valor(int(p))
                self.dger.inicio_teste_convergencia = inicio
                return self.dger
        except Exception:
            print_exc()
            return self.dger

    def _fim_arquivo(self, linha: str) -> bool:
        return False
