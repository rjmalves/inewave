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
from .modelos.dger import EnumSazonaliza
from .modelos.dger import EnumRepresentacaoIncerteza
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

                def le_parametro(linha: str):
                    aux = linha[:21]
                    param = linha[ci:cf].strip()
                    if "TIPO DE EXECUCAO" in aux:
                        t = EnumTipoExecucao.infere_valor(int(param))
                        self.dger.tipo_execucao = t
                    elif "DURACAO DO PERIODO" in aux:
                        self.dger.duracao_estagio_op = int(param)
                    elif "No. DE ANOS DO EST" in aux:
                        self.dger.num_anos_estudo = int(param)
                    elif "MES INICIO PRE-EST" in aux:
                        self.dger.mes_inicio_pre_estudo = int(param)
                    elif "MES INICIO DO ESTUDO" in aux:
                        self.dger.mes_inicio_estudo = int(param)
                    elif "ANO INICIO DO ESTUDO" in aux:
                        self.dger.ano_inicio_estudo = int(param)
                    elif "No. DE ANOS PRE" in aux:
                        self.dger.num_anos_pre_estudo = int(param)
                    elif "No. DE ANOS POS FINAL" in aux:
                        self.dger.num_anos_pos_sim_final = int(param)
                    elif ("No. DE ANOS POS" in aux and "FINAL" not in aux):
                        self.dger.num_anos_pos_estudo = int(param)
                    elif "IMPRIME DADOS" in aux:
                        p = param
                        self.dger.imprime_dados_usinas = (True if p == "1"
                                                          else False)
                    elif "IMPRIME MERCADOS" in aux:
                        p = param
                        self.dger.imprime_dados_mercados = (True if p == "1"
                                                            else False)
                    elif "IMPRIME ENERGIAS" in aux:
                        p = param
                        self.dger.imprime_dados_energias = (True if p == "1"
                                                            else False)
                    elif "IMPRIME M. ESTOCAS" in aux:
                        p = param
                        self.dger.imprime_dados_modelo = (True if p == "1"
                                                          else False)
                    elif "IMPRIME SUBSISTEMA" in aux:
                        p = param
                        self.dger.imprime_dados_rees = (True if p == "1"
                                                        else False)
                    elif "No MAX. DE ITER." in aux:
                        self.dger.max_iteracoes = int(param)
                    elif "No DE SIM. FORWARD" in aux:
                        self.dger.num_sim_forward = int(param)
                    elif "No DE ABERTURAS" in aux:
                        self.dger.num_aberturas = int(param)
                    elif "No DE SERIES SINT." in aux:
                        self.dger.num_series_sinteticas = int(param)
                    elif "ORDEM MAX. PAR(P)" in aux:
                        self.dger.ordem_maxima_parp = int(param)
                    elif "ANO INICIAL HIST." in aux:
                        self.dger.ano_inicial_vaz_historicas = int(param)
                        t = int(linha[28])
                        tam = EnumTamanhoArquivoVazoes.infere_valor(t)
                        self.dger.tamanho_arq_vaz_historicas = tam
                    elif "CALCULA VOL.INICIAL" in aux:
                        p = param
                        self.dger.calcula_vol_inicial = (True if p == "1"
                                                         else False)
                    elif "VOLUME INICIAL  -%" in aux:
                        pass
                    elif "POR SUBSISTEMA" in aux:
                        cisub = 22
                        n_col_sub = 5
                        for i in range(4):
                            cfsub = cisub + n_col_sub
                            v = float(linha[cisub:cfsub])
                            self.dger.vol_inicial_subsistema[i] = v
                            cisub = cfsub + 2
                    elif "TOLERANCIA      -%" in aux:
                        self.dger.tolerancia = float(param)
                    elif "TAXA DE DESCONTO-%" in aux:
                        self.dger.taxa_de_desconto = float(param)
                    elif "TIPO SIMUL. FINAL" in aux:
                        val = int(param)
                        tipo = EnumTipoSimulacaoFinal.infere_valor(val)
                        self.dger.tipo_simulacao_final = tipo
                    elif "IMPRESSAO DA OPER" in aux:
                        val = int(param)
                        impr_op = EnumImpressaoOperacao.infere_valor(val)
                        self.dger.impressao_operacao = impr_op
                    elif "IMPRESSAO DA CONVERG." in aux:
                        val = int(param)
                        impr_c = EnumImpressaoConvergencia.infere_valor(val)
                        self.dger.impressao_convergencia = impr_c
                    elif "INTERVALO P/ GRAVAR" in aux:
                        self.dger.intervalo_gravacao_relatorio = int(param)
                    elif "No. MIN. ITER." in aux:
                        self.dger.min_interacoes = int(param)
                    elif "RACIONAMENTO PREVENT." in aux:
                        p = param
                        self.dger.racionamento_preventivo = (True if p == "1"
                                                             else False)
                    elif "No. ANOS MANUT.UTE'S" in aux:
                        self.dger.numero_anos_manutencao_UTEs = int(param)
                    elif "TENDENCIA HIDROLOGICA" in aux:
                        val = int(param)
                        tend = EnumTendenciaHidrologica.infere_valor(val)
                        self.dger.tendencia_hidrologica = tend
                    elif "RESTRICA0 DE ITAIPU" in aux:
                        p = param
                        self.dger.restricoes_itaipu = (True if p == "1"
                                                       else False)
                    elif "BID " in aux:
                        p = param
                        self.dger.bidding_demanda = (True if p == "1"
                                                     else False)
                    elif "PERDAS P/ TRANSMISSAO" in aux:
                        p = param
                        self.dger.perdas_transmissao = (True if p == "1"
                                                        else False)
                    elif "EL NINO" in aux:
                        p = param
                        self.dger.el_nino = (True if p == "1"
                                             else False)
                    elif "ENSO INDEX " in aux:
                        p = param
                        self.dger.enso = (True if p == "1"
                                          else False)
                    elif "DURACAO POR PATAMAR" in aux:
                        val = int(param)
                        dp = EnumDuracaoPatamar.infere_valor(val)
                        self.dger.duracao_patamar = dp
                    elif "OUTROS USOS DA AGUA" in aux:
                        p = param
                        self.dger.considera_desvio_dagua = (True if p == "1"
                                                            else False)
                    elif "CORRECAO DESVIO" in aux:
                        val = int(param)
                        des = EnumCorrecaoEnergiaDesvio.infere_valor(val)
                        self.dger.correcao_energia_desvio = des
                    elif "C.AVERSAO/PENAL.VMINP" in aux:
                        p = param
                        self.dger.considera_curva_aversao = (True if p == "1"
                                                             else False)
                    elif "TIPO DE GERACAO ENAS" in aux:
                        val = int(param)
                        tg = EnumTipoGeracaoENAs.infere_valor(val)
                        self.dger.tipo_geracao_afluencias = tg
                    elif "RISCO DE DEFICIT" in aux:
                        r1 = float(linha[21:25].strip())
                        r2 = float(linha[27:31].strip())
                        self.dger.profundidade_risco_deficit = (r1, r2)
                    elif "ITERACAO P/SIM.FINAL" in aux:
                        self.dger.iteracao_sim_final = int(param)
                    elif "AGRUPAMENTO LIVRE" in aux:
                        p = param
                        self.dger.agrupamento_livre_interc = (True
                                                              if p == "1"
                                                              else False)
                    elif "EQUALIZACAO PEN.INT." in aux:
                        p = param
                        self.dger.equaliza_penalidades_interc = (True
                                                                 if p == "1"
                                                                 else False)
                    elif "REPRESENT.SUBMOT." in aux:
                        t = int(param)
                        sm = EnumRepresentacaoSubmotorizacao.infere_valor(t)
                        self.dger.representa_submotor = sm
                    elif "ORDENACAO AUTOMATICA" in aux:
                        p = param
                        self.dger.ordenacao_automatica_subsist = (True
                                                                  if p == "1"
                                                                  else False)
                    elif "CONS. CARGA ADICIONAL" in aux:
                        p = param
                        self.dger.considera_cargas_adicionais = (True
                                                                 if p == "1"
                                                                 else False)
                    elif "DELTA ZSUP" in aux:
                        self.dger.delta_zsup = float(param)
                    elif "DELTA ZINF" in aux:
                        self.dger.delta_zinf = float(param)
                    elif "DELTAS CONSECUT." in aux:
                        self.dger.deltas_consecutivos = int(param)
                    elif "DESP. ANTEC.  GNL" in aux:
                        p = param
                        self.dger.considera_despacho_gnl = (True
                                                            if p == "1"
                                                            else False)
                    elif "MODIF.AUTOM.ADTERM" in aux:
                        p = param
                        self.dger.modifica_auto_despacho_gnl = (True
                                                                if p == "1"
                                                                else False)
                    elif "CONSIDERA GHMIN" in aux:
                        p = param
                        self.dger.considera_ghmin = (True
                                                     if p == "1"
                                                     else False)
                    elif "S.F. COM DATA" in aux:
                        p = param
                        self.dger.sim_final_com_data = (True
                                                        if p == "1"
                                                        else False)
                    elif "GER.PLs E NV1 E NV2" in aux:
                        p1 = linha[21:25].strip()
                        p2 = linha[26:30].strip()
                        p3 = linha[31:35].strip()
                        p4 = linha[36:40].strip()
                        p5 = linha[41:45].strip()
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
                    elif "SAR" in aux:
                        p = param
                        self.dger.sar = (True if p == "1"
                                         else False)
                    elif "CVAR" in aux:
                        p = param
                        self.dger.cvar = (True if p == "1"
                                          else False)
                    elif "CONS. ZSUP MIN. CONV." in aux:
                        p = param
                        self.dger.convergencia_minimo_zsup = (True if p == "1"
                                                              else False)
                    elif "DESCONSIDERA VAZMIN" in aux:
                        p = param
                        self.dger.desconsidera_vazao_minima = (True if p == "1"
                                                               else False)
                    elif "RESTRICOES ELETRICAS" in aux:
                        p = param
                        self.dger.considera_restricoes_elet = (True if p == "1"
                                                               else False)
                    elif "SELECAO DE CORTES" in aux:
                        p = param
                        self.dger.selecao_cortes_benders = (True if p == "1"
                                                            else False)
                    elif "JANELA DE CORTES" in aux:
                        p = param
                        self.dger.janela_selecao_cortes = (True if p == "1"
                                                           else False)
                    elif "REAMOST. CENARIOS" in aux:
                        reamos = linha[21:25].strip()
                        self.dger.reamostragem = bool(int(reamos))
                        reamos = linha[26:30].strip()
                        t = int(reamos)
                        tipo_reamos = EnumTipoReamostragem.infere_valor(t)
                        self.dger.tipo_reamostragem = tipo_reamos
                        self.dger.passo_reamostragem = int(linha[31:35])
                    elif "CONVERGE NO ZERO" in aux:
                        p = param
                        self.dger.considera_convergencia_no0 = (True
                                                                if p == "1"
                                                                else False)
                    elif "CONSULTA FCF" in aux:
                        p = param
                        self.dger.consulta_fcf = (True
                                                  if p == "1"
                                                  else False)
                    elif "IMPRESSAO ENA" in aux:
                        self.dger.impressao_ena = bool(int(param))
                    elif "IMP. CATIVO S.FINAL" in aux:
                        self.dger.impressao_cortes_ativos = bool(int(param))
                    elif "REP. AGREGACAO" in aux:
                        t = int(param)
                        ra = EnumRepresentanteAgregacao.infere_valor(t)
                        self.dger.representante_agregacao = ra
                    elif "MATRIZ CORR.ESPACIAL" in aux:
                        t = int(param)
                        mc = EnumMatrizCorrelacaoEspacial.infere_valor(t)
                        self.dger.matriz_corr_espacial = mc
                    elif "DESCONS. CONV. ESTAT" in aux:
                        p = param
                        self.dger.desconsidera_converg_estatist = bool(int(p))
                    elif "MOMENTO REAMOSTRAGEM" in aux:
                        t = int(param)
                        mr = EnumMomentoReamostragem.infere_valor(t)
                        self.dger.momento_reamostragem = mr
                    elif "ARQUIVOS ENA" in aux:
                        p = param
                        self.dger.mantem_arquivos_ena = bool(int(p))
                    elif "INICIO TESTE CONVERG." in aux:
                        t = int(param)
                        tc = EnumInicioTesteConvergencia.infere_valor(t)
                        self.dger.inicio_teste_convergencia = tc
                    elif "SAZ. VMINT PER. EST." in aux:
                        t = int(param)
                        sv = EnumSazonaliza.infere_valor(t)
                        self.dger.sazonaliza_vmint = sv
                    elif "SAZ. VMAXT PER. EST." in aux:
                        t = int(param)
                        sv = EnumSazonaliza.infere_valor(t)
                        self.dger.sazonaliza_vmaxt = sv
                    elif "SAZ. VMINP PER. EST." in aux:
                        t = int(param)
                        sv = EnumSazonaliza.infere_valor(t)
                        self.dger.sazonaliza_vminp = sv
                    elif "SAZ. CFUGA e CMONT" in aux:
                        t = int(param)
                        sv = EnumSazonaliza.infere_valor(t)
                        self.dger.sazonaliza_cfuga_cmont = sv
                    elif "REST. EMISSAO GEE" in aux:
                        p = param
                        self.dger.restricoes_gee = bool(int(p))
                    elif "AFLUENCIA ANUAL PARP" in aux:
                        af1 = bool(int(linha[21:25].strip()))
                        af2 = bool(int(linha[26:30].strip()))
                        self.dger.afluencia_anual_parp = (af1, af2)
                    elif "INCERTEZA GER.EOLICA" in aux:
                        p = param
                        self.dger.incerteza_ger_eolica = bool(int(p))
                    elif "INCERTEZA GER.SOLAR" in aux:
                        p = param
                        self.dger.incerteza_ger_solar = bool(int(p))
                    elif "REPRESENTACAO INCERT" in aux:
                        t = int(param)
                        ri = EnumRepresentacaoIncerteza.infere_valor(t)
                        self.dger.representacao_incerteza = ri
                    elif "REST. FORNEC. GAS" in aux:
                        p = param
                        self.dger.restricoes_fornecimento_gas = bool(int(p))

                while True:
                    # Confere se o arquivo já acabou
                    linha = self._le_linha_com_backup(arq)
                    if len(linha) < 2:
                        break
                    # Senão, lê mais um parâmetro
                    le_parametro(linha)
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
            # Sazonalização Vmint
            escreve_alinhado("SAZ. VMINT PER. EST.",
                             dger.sazonaliza_vmint.value)
            # Sazonalização Vmaxt
            escreve_alinhado("SAZ. VMAXT PER. EST.",
                             dger.sazonaliza_vmaxt.value)
            # Sazonalização Vminp
            escreve_alinhado("SAZ. VMINP PER. EST.",
                             dger.sazonaliza_vminp.value)
            # Sazonalização Cfuga e Cmont
            escreve_alinhado("SAZ. CFUGA e CMONT",
                             dger.sazonaliza_cfuga_cmont.value)
            # Restrições de GEE
            escreve_alinhado("REST. EMISSAO GEE",
                             dger.restricoes_gee)
            # Uso do PAR(p)-A
            str_aux = "AFLUENCIA ANUAL PARP".ljust(len_aux)
            str_dados = ""
            d = int(dger.afluencia_anual_parp[0])
            str_dados += str(int(d)).rjust(4) + " "
            d = int(dger.afluencia_anual_parp[1])
            str_dados += str(int(d)).rjust(4)
            arq.write(str_aux + str_dados + "\n")
            # Incerteza na geração eólica
            escreve_alinhado("INCERTEZA GER.EOLICA",
                             dger.incerteza_ger_eolica)
            # Incerteza na geração solar
            escreve_alinhado("INCERTEZA GER.SOLAR",
                             dger.incerteza_ger_solar)
            # Representação das incertezas
            escreve_alinhado("REPRESENTACAO INCERT",
                             dger.representacao_incerteza.value)
            # Restrições de fornecimento de gás
            escreve_alinhado("REST. FORNEC. GAS",
                             dger.restricoes_fornecimento_gas)
