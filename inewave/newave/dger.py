# Imports do próprio módulo
from inewave._utils.escrita import Escrita
from inewave._utils.leitura import Leitura
from .modelos.dger import DGer
from .modelos.dger import EnumImpressaoConvergencia
from .modelos.dger import EnumImpressaoOperacao
from .modelos.dger import EnumTamanhoArquivoVazoes
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
    Realiza a leitura do arquivo dger.dat
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo dger.dat, construindo
    um objeto `DGer` cujas informações são as mesmas do dger.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `dger`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraDGer(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> dger = leitor.dger

    """
    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # DGer default, depois é substituído
        self.dger = DGer.dger_padrao()

    def le_arquivo(self) -> DGer:
        """
        Realiza a leitura do arquivo `dger.dat`.
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
                tam = EnumTamanhoArquivoVazoes.infere_valor(int(p[28]))
                self.dger.tamanho_arq_vaz_historicas = tam
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
                impr_op = EnumImpressaoOperacao.infere_valor(int(p))
                self.dger.impressao_operacao = impr_op
                p = le_parametro()
                impr_conv = EnumImpressaoConvergencia.infere_valor(int(p))
                self.dger.impressao_convergencia = impr_conv
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
                self.dger.desconsidera_vazao_minima = (True if p == "1"
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


class EscritaDGer(Escrita):
    """
    Realiza a escrita do arquivo dger.dat
    em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para escrever os campos
    de um arquivo dger.dat, a partir de um objeto `DGer`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de armazenar as strings auxiliares do arquivo, desenhar tabelas, dentre
    outras tarefas associadas à escrita.

    Se o diretório de escrita não existir, ele será criado.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> dger = DGer.dger_padrao()
    >>> escritor = EscritaDGer(diretorio)
    >>> escritor.escreve_arquivo(dger)
    """
    def __init__(self, diretorio: str):
        super().__init__()
        self.diretorio = diretorio

    def escreve_arquivo(self, dger: DGer):
        """
        Realiza a escrita de um arquivo `dger.dat`.
        """
        # Confere se o diretório existe. Senão, cria.
        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)
        # Inicia a escrita
        caminho = os.path.join(self.diretorio, "dger.dat")
        len_aux = 21
        len_dado = 4
        with open(caminho, "w") as arq:

            def escreve_alinhado(aux: str,
                                 dado):
                str_aux = aux.ljust(len_aux)
                str_dado = str(int(dado)).rjust(len_dado)
                arq.write(str_aux + str_dado + "\n")

            def escreve_alinhado_f(aux: str,
                                   dado):
                str_aux = aux.ljust(len_aux)
                alinhado = "{:.1f}".format(float(dado)).rjust(4)
                str_dado = str(alinhado).rjust(len_dado)
                arq.write(str_aux + str_dado + "\n")

            # Nome do estudo
            if "\n" in dger.nome_estudo:
                arq.write(dger.nome_estudo)
            else:
                arq.write(dger.nome_estudo + "\n")
            # Tipo de execução
            escreve_alinhado("TIPO DE EXECUCAO",
                             dger.tipo_execucao.value)
            # Duração do período
            escreve_alinhado("DURACAO DO PERIODO",
                             dger.duracao_estagio_op)
            # Número de anos do estudo
            escreve_alinhado("No. DE ANOS DO EST",
                             dger.num_anos_estudo)
            # Mês de início do pré-estudo
            escreve_alinhado("MES INICIO PRE-EST",
                             dger.mes_inicio_pre_estudo)
            # Mês de início do estudo
            escreve_alinhado("MES INICIO DO ESTUDO",
                             dger.mes_inicio_estudo)
            # Ano de início do estudo
            escreve_alinhado("ANO INICIO DO ESTUDO",
                             dger.ano_inicio_estudo)
            # Número de anos pré estudo
            escreve_alinhado("No. DE ANOS PRE",
                             dger.num_anos_pre_estudo)
            # Número de anos pós-estudo
            escreve_alinhado("No. DE ANOS POS",
                             dger.num_anos_pos_estudo)
            # Número de anos pós na sim. final
            escreve_alinhado("No. DE ANOS POS FINAL",
                             dger.num_anos_pos_sim_final)
            # Imprime dados de usinas
            escreve_alinhado("IMPRIME DADOS",
                             dger.imprime_dados_usinas)
            # Imprime dados de mercados
            escreve_alinhado("IMPRIME MERCADOS",
                             dger.imprime_dados_mercados)
            # Imprime energias
            escreve_alinhado("IMPRIME ENERGIAS",
                             dger.imprime_dados_energias)
            # Imprime dados do modelo
            escreve_alinhado("IMPRIME M. ESTOCAS",
                             dger.imprime_dados_modelo)
            # Imprime dados REEs
            escreve_alinhado("IMPRIME SUBSISTEMA",
                             dger.imprime_dados_rees)
            # Máximo de iterações
            escreve_alinhado("No MAX. DE ITER.",
                             dger.max_iteracoes)
            # Número de forwards
            escreve_alinhado("No DE SIM. FORWARD",
                             dger.num_sim_forward)
            # Número de aberturas
            escreve_alinhado("No DE ABERTURAS",
                             dger.num_aberturas)
            # Número de séries sintéticas
            escreve_alinhado("No DE SERIES SINT.",
                             dger.num_series_sinteticas)
            # Ordem máxima PAR(p)
            escreve_alinhado("ORDEM MAX. PAR(P)",
                             dger.ordem_maxima_parp)
            # Ano inicial do histórico
            str_aux = "ANO INICIAL HIST.".ljust(len_aux)
            ano = dger.ano_inicial_vaz_historicas
            str_dado1 = str(int(ano)).rjust(len_dado)
            tam = dger.tamanho_arq_vaz_historicas.value
            str_dado2 = str(int(tam)).rjust(len_dado)
            arq.write(str_aux + str_dado1 + str_dado2 + "\n")
            # Calcula volume inicial
            escreve_alinhado("CALCULA VOL.INICIAL",
                             dger.calcula_vol_inicial)
            # Linha de cabeçalho
            lin = "VOLUME INICIAL  -%   XXX.X  XXX.X  XXX.X  XXX.X  XXX.X"
            arq.write(lin + "\n")
            # Volumes por subsistema
            str_aux = " POR SUBSISTEMA".ljust(len_aux)
            str_dados = ""
            for v in dger.vol_inicial_subsistema:
                str_dados += "{:.1f}".format(v).rjust(5) + "  "
            arq.write(str_aux + str_dados + "\n")
            # Tolerância
            escreve_alinhado_f("TOLERANCIA      -%",
                               dger.tolerancia)
            # Taxa de desconto
            escreve_alinhado_f("TAXA DE DESCONTO-%",
                               dger.taxa_de_desconto)
            # Tipo de sim final
            escreve_alinhado("TIPO SIMUL. FINAL",
                             dger.tipo_simulacao_final.value)
            # Imprime operação
            escreve_alinhado("IMPRESSAO DA OPER",
                             dger.impressao_operacao.value)
            # Imprime convergência
            escreve_alinhado("IMPRESSAO DA CONVERG.",
                             dger.impressao_convergencia.value)
            # Intervalo gravação
            escreve_alinhado("INTERVALO P/ GRAVAR",
                             dger.intervalo_gravacao_relatorio)
            # Min. iterações
            escreve_alinhado("No. MIN. ITER.",
                             dger.min_interacoes)
            # Racionamento preventivo
            escreve_alinhado("RACIONAMENTO PREVENT.",
                             dger.racionamento_preventivo)
            # Num. anos manutenção UTEs
            escreve_alinhado("No. ANOS MANUT.UTE'S",
                             dger.numero_anos_manutencao_UTEs)
            # Tendência hidrológica
            escreve_alinhado("TENDENCIA HIDROLOGICA",
                             dger.tendencia_hidrologica.value)
            # Restrição de Itaipu
            escreve_alinhado("RESTRICA0 DE ITAIPU",
                             dger.restricoes_itaipu)
            # Bidding
            escreve_alinhado("BID",
                             dger.bidding_demanda)
            # Perdas na transmissão
            escreve_alinhado("PERDAS P/ TRANSMISSAO",
                             dger.perdas_transmissao)
            # El Niño
            escreve_alinhado("EL NINO",
                             dger.el_nino)
            # ENSO
            escreve_alinhado("ENSO INDEX",
                             dger.enso)
            # Duração por patamar
            escreve_alinhado("DURACAO POR PATAMAR",
                             dger.duracao_patamar.value)
            # Considera desvio d'água
            escreve_alinhado("OUTROS USOS DA AGUA",
                             dger.considera_desvio_dagua)
            # Correção do desvio
            escreve_alinhado("CORRECAO DESVIO",
                             dger.correcao_energia_desvio.value)
            # Considera curva VminP
            escreve_alinhado("C.AVERSAO/PENAL.VMINP",
                             dger.considera_curva_aversao)
            # Tipo de geração de ENAs
            escreve_alinhado("TIPO DE GERACAO ENAS",
                             dger.tipo_geracao_afluencias.value)
            # Profundidade do risco de déficit
            str_aux = "RISCO DE DEFICIT".ljust(len_aux)
            str_dados = ""
            for v in dger.profundidade_risco_deficit:
                str_dados += "{:.1f}".format(v).rjust(4) + "  "
            arq.write(str_aux + str_dados + "\n")
            # Iteração para simulação final
            escreve_alinhado("ITERACAO P/SIM.FINAL",
                             dger.iteracao_sim_final)
            # Agrupamento livre de intercâmbios
            escreve_alinhado("AGRUPAMENTO LIVRE",
                             dger.agrupamento_livre_interc)
            # Equalização da penalização de intercâmbios
            escreve_alinhado("EQUALIZACAO PEN.INT.",
                             dger.equaliza_penalidades_interc)
            # Representação da submotorização
            escreve_alinhado("REPRESENT.SUBMOT.",
                             dger.representa_submotor.value)
            # Ordenação automática de subsistemas
            escreve_alinhado("ORDENACAO AUTOMATICA",
                             dger.ordenacao_automatica_subsist)
            # Considera cargas adicionais
            escreve_alinhado("CONS. CARGA ADICIONAL",
                             dger.considera_cargas_adicionais)
            # Delta Zsup
            escreve_alinhado_f("DELTA ZSUP",
                               dger.delta_zsup)
            # Delta Zinf
            escreve_alinhado_f("DELTA ZINF",
                               dger.delta_zinf)
            # Deltas consecutivos
            escreve_alinhado("DELTAS CONSECUT.",
                             dger.deltas_consecutivos)
            # Despacho antecipado GNL
            escreve_alinhado("DESP. ANTEC.  GNL",
                             dger.considera_despacho_gnl)
            # Modifica automaticamente AdTerm
            escreve_alinhado("MODIF.AUTOM.ADTERM",
                             dger.modifica_auto_despacho_gnl)
            # Considera GHmin
            escreve_alinhado("CONSIDERA GHMIN",
                             dger.considera_ghmin)
            # Simulação final com data
            escreve_alinhado("S.F. COM DATA",
                             dger.sim_final_com_data)
            # Gerenciados externo, etc...
            str_aux = "GER.PLs E NV1 E NV2".ljust(len_aux)
            str_dados = ""
            d = int(dger.gerenciador_externo)
            str_dados += str(d).rjust(4) + " "
            d = int(dger.comunicacao_dois_niveis)
            str_dados += str(d).rjust(4) + " "
            d = int(dger.armazenamento_local_temp)
            str_dados += str(d).rjust(4) + " "
            d = int(dger.aloca_memoria_enas)
            str_dados += str(d).rjust(4) + " "
            d = int(dger.aloca_memoria_cortes)
            str_dados += str(d).rjust(4) + " "
            arq.write(str_aux + str_dados + "\n")
            # SAR
            escreve_alinhado("SAR",
                             dger.sar)
            # CVaR
            escreve_alinhado("CVAR",
                             dger.cvar)
            # Critério de min Zsup p/ convergência
            escreve_alinhado("CONS. ZSUP MIN. CONV.",
                             dger.convergencia_minimo_zsup)
            # Desconsidera vazão mínima
            escreve_alinhado("DESCONSIDERA VAZMIN",
                             dger.desconsidera_vazao_minima)
            # Considera restrições elétricas
            escreve_alinhado("RESTRICOES ELETRICAS",
                             dger.considera_restricoes_elet)
            # Seleção de cortes
            escreve_alinhado("SELECAO DE CORTES",
                             dger.selecao_cortes_benders)
            # Janela para seleção de cortes
            escreve_alinhado("JANELA DE CORTES",
                             dger.janela_selecao_cortes)
            # Reamostragem de cenários
            str_aux = "REAMOST. CENARIOS".ljust(len_aux)
            str_dados = ""
            d = int(dger.reamostragem)
            str_dados += str(int(d)).rjust(4) + " "
            d = int(dger.tipo_reamostragem.value)
            str_dados += str(int(d)).rjust(4) + " "
            d = int(dger.passo_reamostragem)
            str_dados += str(int(d)).rjust(4) + " "
            arq.write(str_aux + str_dados + "\n")
            # Considera nó 0 na convergência
            escreve_alinhado("CONVERGE NO ZERO",
                             dger.considera_convergencia_no0)
            # Consulta FCF
            escreve_alinhado("CONSULTA FCF",
                             dger.consulta_fcf)
            # Impressão ENA
            escreve_alinhado("IMPRESSAO ENA",
                             dger.impressao_ena)
            # Impressão de cortes ativos na simulação final
            escreve_alinhado("IMP. CATIVO S.FINAL",
                             dger.impressao_cortes_ativos)
            # Representante da agregação
            escreve_alinhado("REP. AGREGACAO",
                             dger.representante_agregacao.value)
            # Matriz de correlação espacial
            escreve_alinhado("MATRIZ CORR.ESPACIAL",
                             dger.matriz_corr_espacial.value)
            # Desconsidera convergência estatística
            escreve_alinhado("DESCONS. CONV. ESTAT",
                             dger.desconsidera_converg_estatist)
            # Momento da reamostragem
            escreve_alinhado("MOMENTO REAMOSTRAGEM",
                             dger.momento_reamostragem.value)
            # Mantém arquivos ENA
            escreve_alinhado("ARQUIVOS ENA",
                             dger.mantem_arquivos_ena)
            # Início do teste de convergência
            escreve_alinhado("INICIO TESTE CONVERG.",
                             dger.inicio_teste_convergencia.value)
