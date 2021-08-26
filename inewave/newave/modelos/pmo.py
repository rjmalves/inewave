# Imports do próprio módulo
from inewave._utils.bloco import Bloco
from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave._utils.leitura import Leitura
from inewave.config import MAX_ANOS_ESTUDO, MAX_CONFIGURACOES, MAX_ITERS
from inewave.config import REES, NUM_CONFIGS_DGER
from inewave.config import MESES, MESES_DF, SUBMERCADOS
# Imports de módulos externos
from datetime import timedelta
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import IO, List


class BlocoEcoDgerPMO(Bloco):
    """
    Bloco de informações de eco dos dados gerais de execução
    existentes no arquivo `pmo.dat`.
    """

    str_inicio = "  DADOS GERAIS"
    str_fim = "CEPEL"

    nomes_params = [
                    "DURACAO DE CADA PERIODO DE OPERACAO",
                    "NUMERO DE ANOS DO HORIZONTE DE ESTUDO",
                    "MES INICIAL DO PERIODO DE PRE-ESTUDO",
                    "MES INICIAL DO PERIODO DE ESTUDO",
                    "ANO INICIAL DO PERIODO DE ESTUDO",
                    "NUMERO DE ANOS QUE PRECEDEM O HORIZONTE DE ESTUDO",
                    "NUMERO DE ANOS QUE SUCEDEM O HORIZONTE DE ESTUDO",
                    "NUMERO DE ANOS DO POS NA SIMULACAO FINAL",
                    "IMPRIME DADOS DAS USINAS",
                    "IMPRIME DADOS DE MERCADO",
                    "IMPRIME DADOS DE ENERGIAS",
                    "IMPRIME PARAMETROS DO MODELO DE ENERGIA",
                    "IMPRIME PARAMETROS DO RESERVATORIO EQUIVALENTE",
                    "IMPRIME DETALHAMENTO DA OPERACAO",
                    "IMPRIME DETALHAMENTO DO CALCULO DA POLITICA",
                    "IMPRIME RESULTADOS DA CONVERGENCIA",
                    "NUMERO MAXIMO DE ITERACOES",
                    "NUMERO DE SIMULACOES",
                    "NUMERO DE ABERTURAS",
                    "ORDEM MAXIMA DO MODELO DE ENERGIAS AFLUENTES PAR(P)",
                    "ANO INICIAL DO HISTORICO DE VAZOES",
                    "CALCULA VOLUME INICIAL",
                    "TOLERANCIA PARA CONVERGENCIA",
                    "TAXA DE DESCONTO ANUAL (%)",
                    "TOTAL DE SERIES SIMULADAS GRAVADAS",
                    "NUMERO MINIMO DE ITERACOES PARA CONVERGENCIA",
                    "ADOCAO DE RACIONAMENTO PREVENTIVO (SIM.FINAL)",
                    "LIDA DO ARQUIVO DE MANUTENCOES",
                    "ADOCAO DE TENDENCIA HIDROLOGICA (POLITICA)",
                    "ADOCAO DE TENDENCIA HIDROLOGICA (SIMULACAO FINAL)",
                    "CONSIDERA OUTROS USOS DA AGUA",
                    "OUTROS USOS DA AGUA VARIAVEL COM A ENERGIA ARMAZENADA",
                    "CONSIDERA CURVA GUIA DE SEGURANCA/VMINP",
                    "TAMANHO DA AMOSTRA PARA PROCESSO DE AGREGACAO:",
                    "REPRESENTANTE NO PROCESSO DE AGREGACAO:",
                    "MATRIZ DE CORRELACAO ESPACIAL CONSIDERADA:",
                    "DESCONSIDERA CRITERIO DE CONV. ESTATISTICO",
                    "VOLUME MINIMO COM DATA SAZONAL NOS PERIODOS ESTATICOS",
                    "VOLUME MAXIMO COM DATA SAZONAL NOS PERIODOS ESTATICOS",
                    "VOLUME MAXIMO PENAL. SAZONAL NOS PERIODOS ESTATICOS",
                    "CFUGA E CMONT SAZONAIS NOS PERIODOS ESTATICOS",
                    " - CENARIOS DE ENERGIA:",
                    " - CORTES ATIVOS:",
                    "MANTEM OS ARQUIVOS DE ENERGIAS APOS EXECUCAO:",
                    "MOMENTO DE REAMOSTRAGEM:",
                    "CONSIDERA VERIFICACAO AUTOMATICA DA ORDEM DO MODELO PARP:",  # noqa
                    "ITERACAO DE INICIO DO TESTE DE CONVERGENCIA",
                    "PROF. DE MERCADO PARA CALCULO DO RISCO DE DEFICIT",
                    "CONSIDERA AGRUPAMENTO DE INTERCAMBIOS",
                    "CONSIDERA EQUALIZACAO DE PENALIDADES DE INTERCAMBIOS",
                    "CONSIDERA SUBMOTORIZACAO SAZONAL",
                    "CONSIDERA ORDENACAO AUTOMATICA REEs, SUBSISTEMAS E TERMICAS",  # noqa
                    "CONSIDERA CARGAS ADICIONAIS",
                    "  - DELTA DE ZSUP",
                    "  - DELTA DE ZINF",
                    "  - NUMERO DE DELTAS DE ZINF CONSECUTIVOS",
                    "  - MINIMO ZSUP",
                    "CONSIDERA ANTECIPACAO DE GERACAO TERMOELETRICA",
                    "ANTECIPACAO DE GERACAO TERMOELETRICA",
                    "CONSIDERA GERACAO HIDRAULICA MINIMA",
                    "CONSIDERA GERENCIAMENTO EXTERNO DE PROCESSOS",
                    "CONSIDERA COMUNICACAO EM DOIS NIVEIS",
                    "CONSIDERA ARMAZENAMENTO LOCAL DE ARQUIVOS",
                    "CONSIDERA ALOCACAO DE ENERGIA EM MEMORIA",
                    "CONSIDERA ALOCACAO DE CORTES EM MEMORIA",
                    "CONSIDERA SUPERFICIE DE AVERSAO A RISCO (SAR)",
                    "CONSIDERA MECANISMO DE AVERSAO AO RISCO (CVAR)",
                    "DESCONSIDERA VAZAO MINIMA",
                    "CONSIDERA RESTRICOES ELETRICAS NO REE",
                    "CONSIDERA PERDAS NA REDE DE TRANSMISSAO",
                    "CONSIDERA SELECAO DE CORTES DE BENDERS",
                    "CONSIDERA JANELA DE CORTES DE BENDERS",
                    "IMPRIME ESTADOS QUE GERARAM OS CORTES",
                    "CONSIDERA REAMOSTRAGEM DE CENARIOS",
                    "     PASSO DA REAMOSTRAGEM:",
                    "     TIPO DA REAMOSTRAGEM :",
                    "CONSIDERA ZINF CALCULADO NO NO ZERO",
                    "REALIZA ACESSO A FCF PARA CONVERGENCIA",
                    "CONSIDERA AFLUENCIA ANUAL NOS MODELOS",
                    "CONSIDERA RESTRICOES DE LIMITES DE EMISSAO DE GEE",
                    "CONSIDERA RESTRICOES DE FORNECIMENTO DE GAS",
                    "CONSIDERACAO DA INCERTEZA NA GERACAO EOLICA",
                    "CONSIDERACAO DA INCERTEZA NA GERACAO SOLAR",
                    "CONSIDERA DEPENDENCIA TEMPORAL DAS AFLUENCIAS NA PDDE"
                   ]

    def __init__(self):
        super().__init__(BlocoEcoDgerPMO.str_inicio,
                         BlocoEcoDgerPMO.str_fim,
                         True)
        self._dados = np.zeros((NUM_CONFIGS_DGER,),
                               dtype=np.float64)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoEcoDgerPMO):
            return False
        bloco: BlocoEcoDgerPMO = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):

        def __le_eco_config(digitos: int) -> str:
            """
            Lê o eco de uma configuração, pulando uma linha em seguida.
            """
            linha: str = arq.readline()
            arq.readline()
            return linha.strip()[-digitos:].strip()

        def __le_sim_nao(i: int) -> int:
            """
            Interpreta os campos de configurações SIM e NAO.
            """
            dado = __le_eco_config(4)
            if "SIM" in dado:
                self._dados[i] = 1.0
            elif "NAO" in dado:
                self._dados[i] = 0.0
            else:
                raise ValueError(f"Valor {dado} inválido para SIM ou NAO")
            return i + 1

        def __le_numerico(i: int, digitos: int) -> int:
            dado = __le_eco_config(digitos)
            self._dados[i] = float(dado)
            return i + 1

        # Pula as duas primeiras linhas
        arq.readline()
        arq.readline()
        # Variáveis auxiliares
        i = 0
        # Duração de cada período de operação
        i = __le_numerico(i, 3)
        # Número de anos do horizonte
        i = __le_numerico(i, 3)
        # Mês inicial do pré-estudo
        i = __le_numerico(i, 3)
        # Mês inicial do estudo
        i = __le_numerico(i, 3)
        # Ano inicial do estudo
        i = __le_numerico(i, 6)
        # Anos pre estudo
        i = __le_numerico(i, 3)
        # Anos pos estudo
        i = __le_numerico(i, 3)
        # Anos pos estudos na sim. final
        i = __le_numerico(i, 3)
        # Imprime dados usinas
        i = __le_sim_nao(i)
        # Imprime dados mercado
        i = __le_sim_nao(i)
        # Imprime dados energias
        i = __le_sim_nao(i)
        # Imprime parametros modelo energia
        i = __le_sim_nao(i)
        # Imprime parametros reservatorio equivalente
        i = __le_sim_nao(i)
        # Imprime detalhamento da operação
        i = __le_sim_nao(i)
        # Imprime detalhamento calc. política
        i = __le_sim_nao(i)
        # Imprime resultados convergência
        i = __le_sim_nao(i)
        # Max. iterações
        i = __le_numerico(i, 4)
        # Num. forwards
        i = __le_numerico(i, 6)
        # Num. aberturas
        i = __le_numerico(i, 6)
        # Ordem máxima PAR(p)
        i = __le_numerico(i, 4)
        # Ano inicial histórico
        i = __le_numerico(i, 6)
        # Calcula vol. inic.
        i = __le_sim_nao(i)
        arq.readline()
        # Tolerância convergência
        i = __le_numerico(i, 6)
        # Taxa de desconto
        i = __le_numerico(i, 9)
        # Séries simuladas gravadas
        arq.readline()
        i = __le_numerico(i, 6)
        arq.readline()
        # Min. iterações
        i = __le_numerico(i, 6)
        # Racionamento preventivo
        i = __le_sim_nao(i)
        # Num. anos com manut. térmicas
        arq.readline()
        i = __le_numerico(i, 3)
        # Tendência hidrológica (política)
        i = __le_sim_nao(i)
        # Tendência hidrológica (sim. final)
        i = __le_sim_nao(i)
        # Considera desvio de agua
        i = __le_sim_nao(i)
        # Outros usos variável com EARM
        i = __le_sim_nao(i)
        # Considera curva (VminP)
        i = __le_sim_nao(i)
        # Tamanho da amostra para agregação
        arq.readline()
        i = __le_numerico(i, 7)
        # Representante no processo
        repr = 1.0 if "CENTROIDE" in __le_eco_config(10) else 0.0
        self._dados[i] = repr
        i += 1
        # Matriz de correlação considerada
        corr = 0.0 if "ANUAL" in __le_eco_config(6) else 0.0
        self._dados[i] = corr
        i += 1
        # Desconsidera critério de convergência
        i = __le_sim_nao(i)
        # Vol. min. sazonal nos períodos estáticos
        i = __le_sim_nao(i)
        # Vol. max. sazonal nos períodos estáticos
        i = __le_sim_nao(i)
        # Vol. max. penal. sazonal os períodos estáticos
        i = __le_sim_nao(i)
        # Cfuga e Cmont sazonais nos períodos estáticos
        i = __le_sim_nao(i)
        # Imprime cenários energia
        arq.readline()
        self._dados[i] = 0.0 if "NAO" in arq.readline()[-5].strip() else 1.0
        i += 1
        # Imprime cortes ativos
        i = __le_sim_nao(i)
        # Mantém energias após execução
        i = __le_sim_nao(i)
        # Momento de reamostragem
        self._dados[i] = 1.0 if "FORWARD" in arq.readline().strip() else 0.0
        arq.readline()
        i += 1
        # Considera redução da ordem PAR(p)
        i = __le_sim_nao(i)
        # Iteração de início do teste de convergência
        i = __le_numerico(i, 4)

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoEafPastTendenciaHidrolPMO(Bloco):
    """
    Bloco de informações de afluências passadas para
    tendência hidrológica localizado no arquivo `pmo.dat`.
    """

    str_inicio = "ENERGIAS AFLUENTES PASSADAS PARA A TENDENCIA HIDROLOGICA"
    str_fim = ""

    def __init__(self):
        super().__init__(BlocoEafPastTendenciaHidrolPMO.str_inicio,
                         BlocoEafPastTendenciaHidrolPMO.str_fim,
                         True)
        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoEafPastTendenciaHidrolPMO):
            return False
        bloco: BlocoEafPastTendenciaHidrolPMO = o
        return self._dados.equals(bloco.dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df():
            df = pd.DataFrame(tabela,
                              columns=MESES_DF)
            df["REE"] = rees
            df = df[["REE"] + MESES_DF]
            return df

        # Pula as linhas iniciais
        for _ in range(3):
            arq.readline()
        # Variáveis auxiliares
        reg_sistema = RegistroAn(10)
        reg_eaf = RegistroFn(8)
        rees: List[str] = []
        tabela = np.zeros((len(REES), len(MESES_DF)))
        i = 0
        while True:
            linha: str = arq.readline()
            # Confere se acabou
            if "X-------" in linha:
                self._dados = converte_tabela_em_df()
                break
            # Lê mais uma linha
            rees.append(reg_sistema.le_registro(linha, 1))
            tabela[i, :] = reg_eaf.le_linha_tabela(linha,
                                                   14,
                                                   3,
                                                   len(MESES))
            i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoEafPastCfugaMedioPMO(Bloco):
    """
    Bloco de informações de afluências passadas para
    tendência hidrológica localizado no arquivo `pmo.dat`.
    """

    str_inicio = "ENERGIAS AFLUENTES PASSADAS EM REFERENCIA A PRIMEIRA CONFIG"
    str_fim = ""

    def __init__(self):
        super().__init__(BlocoEafPastCfugaMedioPMO.str_inicio,
                         BlocoEafPastCfugaMedioPMO.str_fim,
                         True)
        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoEafPastCfugaMedioPMO):
            return False
        bloco: BlocoEafPastCfugaMedioPMO = o
        return self._dados.equals(bloco.dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df():
            df = pd.DataFrame(tabela,
                              columns=MESES_DF)
            df["REE"] = rees
            df = df[["REE"] + MESES_DF]
            return df

        # Pula as linhas iniciais
        for _ in range(3):
            arq.readline()
        # Variáveis auxiliares
        reg_sistema = RegistroAn(10)
        reg_eaf = RegistroFn(8)
        rees: List[str] = []
        tabela = np.zeros((len(REES), len(MESES_DF)))
        i = 0
        while True:
            linha: str = arq.readline()
            # Confere se acabou
            if "X-------" in linha:
                self._dados = converte_tabela_em_df()
                break
            # Lê mais uma linha
            rees.append(reg_sistema.le_registro(linha, 1))
            tabela[i, :] = reg_eaf.le_linha_tabela(linha,
                                                   14,
                                                   3,
                                                   len(MESES))
            i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoConvergenciaPMO(Bloco):
    """
    Bloco com as informações de convergência do NEWAVE obtidas
    no arquivo `pmo.dat`.
    """

    str_inicio = "    ITER               LIM.INF.        "
    str_fim = ""

    def __init__(self):
        super().__init__(BlocoConvergenciaPMO.str_inicio,
                         BlocoConvergenciaPMO.str_fim,
                         True)
        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConvergenciaPMO):
            return False
        bloco: BlocoConvergenciaPMO = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = ["Iteração", "Lim. Inf. ZINF", "ZINF",
                          "Lim. Sup. ZINF", "ZSUP", "Delta ZINF",
                          "ZSUP Iteração", "Tempo (s)"]
            df = df.astype({"Iteração": 'int32'})
            return df

        # Salta as duas linhas iniciais
        arq.readline()
        arq.readline()
        # Variáveis auxiliares
        reg_iter = RegistroIn(4)
        reg_z = RegistroFn(22)
        tabela = np.zeros((3 * MAX_ITERS, 8),
                          dtype=np.float64)
        i = 0
        while True:
            linha: str = arq.readline()
            # Confere se já acabou
            if len(linha) < 3:
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Se não tem nada na coluna de iteração, ignora a linha
            if linha[4:9] == "     ":
                continue
            # Lê a iteração
            tabela[i, 0] = reg_iter.le_registro(linha, 4)
            # Lê os limites e valores de zinf e zsup
            tabela[i, 1:5] = reg_z.le_linha_tabela(linha, 9, 1, 4)
            # Lê delta z inf e zup iter se houver
            if len(linha[101:122].strip()) > 1:
                tabela[i, 5] = reg_z.le_registro(linha, 101)
            if len(linha[123:144].strip()) > 1:
                tabela[i, 6] = reg_z.le_registro(linha, 123)
            # Lê o tempo, convertendo para segundos, se houver
            if "min" in linha[153:168]:
                tempo = linha[153:168]
                h = int(tempo.split("h")[0])
                min = int(tempo.split("h")[1].split("min")[0])
                s = float(tempo.split("min")[1].split("s")[0])
                ts = timedelta(hours=h, minutes=min, seconds=s).total_seconds()
                tabela[i, 7] = ts
            i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoConfiguracoesExpansaoPMO(Bloco):
    """
    Bloco de informações sobre as configurações de expansão
    do sistema existentes no arquivo `pmo.dat`.
    """

    str_inicio = "CONFIGURACOES POR"
    str_fim = ""

    def __init__(self):
        super().__init__(BlocoConfiguracoesExpansaoPMO.str_inicio,
                         BlocoConfiguracoesExpansaoPMO.str_fim,
                         True)
        self._dados = np.zeros((MAX_ANOS_ESTUDO, len(MESES) + 1),
                               dtype=np.int64)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConfiguracoesExpansaoPMO):
            return False
        bloco: BlocoConfiguracoesExpansaoPMO = o
        return np.array_equal(self.dados, bloco.dados)

    # Override
    def le(self, arq: IO):
        # Pula as linhas iniciais
        for _ in range(5):
            arq.readline()
        # Variáveis auxiliares
        reg = RegistroIn(5)
        i = 0
        while True:
            linha: str = arq.readline()
            # Confere se acabou
            if len(linha) < 3:
                self._dados = self._dados[:i, :]
                break
            # Lê mais uma linha
            self._dados[i, :] = reg.le_linha_tabela(linha,
                                                    5,
                                                    1,
                                                    len(MESES) + 1)
            i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoMARSPMO(Bloco):
    """
    Bloco de informações sobre o modelo MARS ajustado
    para as retas de perdas por engolimento máximo
    existentes no arquivo `pmo.dat`.
    """

    str_inicio = "PARAMETROS DAS RETAS DE PERDAS POR ENGOLIMENTO MAXIMO"
    str_fim = 'CEPEL'

    MAX_RETAS_MARS = 3

    def __init__(self):
        super().__init__(BlocoMARSPMO.str_inicio,
                         BlocoMARSPMO.str_fim,
                         True)
        self._dados = np.zeros((BlocoMARSPMO.MAX_RETAS_MARS,
                                2,
                                len(REES)),
                               dtype=np.float64)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoMARSPMO):
            return False
        bloco: BlocoMARSPMO = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):
        # Variáveis auxiliares
        ree = 0
        reg_ree = RegistroAn(10)
        reg_reta = RegistroFn(12)
        rees_lidos = 0
        while True:
            linha: str = arq.readline()
            if rees_lidos == len(REES) or BlocoMARSPMO.str_fim in linha:
                break
            elif "REE:" in linha:
                ree = REES.index(reg_ree.le_registro(linha, 6))
                # Salta linhas entre o título e os coeficientes
                for _ in range(4):
                    arq.readline()
                # Lê as retas disponíveis
                rees_lidos += 1
                for i in range(BlocoMARSPMO.MAX_RETAS_MARS):
                    linha = arq.readline()
                    if len(linha) > 3:
                        self._dados[i,
                                    :,
                                    ree] = reg_reta.le_linha_tabela(linha,
                                                                    14,
                                                                    1,
                                                                    2)

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoRiscoDeficitENSPMO(Bloco):
    """
    Bloco de informações sobre os riscos de déficit e
    ENS (energia não suprida) existentes no arquivo `pmo.dat`.
    """

    str_inicio = " ANO  RISCO   EENS  RISCO"
    str_fim = ""

    def __init__(self):
        super().__init__(BlocoRiscoDeficitENSPMO.str_inicio,
                         BlocoRiscoDeficitENSPMO.str_fim,
                         True)
        self._dados = np.zeros((MAX_ANOS_ESTUDO,
                                2 * len(SUBMERCADOS) + 1),
                               dtype=np.float64)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoRiscoDeficitENSPMO):
            return False
        bloco: BlocoRiscoDeficitENSPMO = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):
        # Pula as duas linhas iniciais
        arq.readline()
        arq.readline()
        # Variáveis auxiliares
        reg_ano = RegistroIn(4)
        reg_risco = RegistroFn(6)
        reg_eens = RegistroFn(8)
        i = 0
        while True:
            linha: str = arq.readline()
            # Confere se acabou
            if len(linha) < 3:
                self._dados = self._dados[:i, :]
                break
            self._dados[i, 0] = reg_ano.le_registro(linha, 1)
            self._dados[i, 1::2] = reg_risco.le_linha_tabela(linha,
                                                             6,
                                                             8,
                                                             len(SUBMERCADOS))
            self._dados[i, 2::2] = reg_eens.le_linha_tabela(linha,
                                                            12,
                                                            6,
                                                            len(SUBMERCADOS))
            i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoCustoOperacaoPMO(Bloco):
    """
    Bloco de informações sobre os custos de operação categorizados
    existentes no arquivo `pmo.dat`.
    """

    str_inicio = "PARCELA           V.ESPERADO"

    componentes_custo = [
                         "GERACAO TERMICA   ",
                         "DEFICIT           ",
                         "VERTIMENTO        ",
                         "EXCESSO ENERGIA   ",
                         "VIOLACAO CAR      ",
                         "VIOLACAO SAR      ",
                         "VIOL. OUTROS USOS ",
                         "VIOLACAO EVMIN    ",
                         "VIOLACAO VZMIN    ",
                         "INTERCAMBIO       ",
                         "VIOL. INTERC. MIN.",
                         "VERT. FIO N. TURB.",
                         "VIOLACAO GHMIN    ",
                         "VIOLACAO GHMINU   ",
                         "VIOLACAO RETIRADA ",
                         "VIOLACAO EMIS. GEE"
                        ]

    def __init__(self):
        super().__init__(BlocoCustoOperacaoPMO.str_inicio,
                         "",
                         True)
        self._dados = np.zeros((len(BlocoCustoOperacaoPMO.componentes_custo),
                                3),
                               dtype=np.float64)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoCustoOperacaoPMO):
            return False
        bloco: BlocoCustoOperacaoPMO = o
        return np.array_equal(self._dados, bloco._dados)

    # Override
    def le(self, arq: IO):
        # Salta uma linha
        arq.readline()
        # Variáveis auxiliares
        reg_valores = RegistroFn(13)
        reg_percent = RegistroFn(7)
        i = 0
        while True:
            linha = arq.readline()
            if "----------------" in linha:
                break
            self._dados[i, :2] = reg_valores.le_linha_tabela(linha,
                                                             32,
                                                             1,
                                                             2)
            self._dados[i, 2] = reg_percent.le_registro(linha, 60)
            i += 1

    # Override
    def escreve(self, arq: IO):
        pass


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

    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo parp.dat.
        """
        # eco_dger: List[Bloco] = [BlocoEcoDgerPMO()]
        convergencia: List[Bloco] = [BlocoConvergenciaPMO()]
        eafpast: List[Bloco] = [BlocoEafPastTendenciaHidrolPMO(),
                                BlocoEafPastCfugaMedioPMO()]
        risco_deficit: List[Bloco] = [BlocoRiscoDeficitENSPMO()]
        configs_exp: List[Bloco] = [BlocoConfiguracoesExpansaoPMO()
                                    for _ in range(3)]
        mars: List[Bloco] = [BlocoMARSPMO()
                             for _ in range(MAX_CONFIGURACOES)]
        custos: List[Bloco] = [
                               BlocoCustoOperacaoPMO(),
                               BlocoCustoOperacaoPMO(),
                               BlocoCustoOperacaoPMO()
                              ]

        return (convergencia +
                eafpast +
                risco_deficit +
                configs_exp +
                mars +
                custos)
