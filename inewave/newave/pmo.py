# Imports do próprio módulo
from inewave._utils.leitura import Leitura
from inewave.config import NUM_ANOS_ESTUDO, NUM_VARIAVEIS_CUSTO_PMO, REES
from inewave.config import MESES, SUBMERCADOS
from .modelos.pmo import DadosGeraisPMO
from .modelos.pmo import EnergiaFioLiquidaREEPMO
from .modelos.pmo import RetasPerdasEngolimentoREEPMO
from .modelos.pmo import EnergiasAfluentesPMO
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
    existente em um diretório de entradas do NEWAVE.

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
    str_inicio_risco = " ANO  RISCO   EENS  RISCO"
    str_inicio_custo_series = "                 CUSTO DE OPERACAO DAS"
    str_inicio_valor_esperado = "                 VALOR ESPERADO PARA PERI"
    str_inicio_custo_referenciado = "                     CUSTO OPERACAO R"
    str_inicio_efio_liquida = '***ENERGIA FIO D"AGUA LIQUIDA***'
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
                       DadosGeraisPMO(),
                       EnergiaFioLiquidaREEPMO(np.array([])),
                       RetasPerdasEngolimentoREEPMO(np.array([])),
                       EnergiasAfluentesPMO(),
                       EnergiasAfluentesPMO(),
                       EnergiasAfluentesPMO(),
                       {},
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
        achou_efio_liquida = False
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
        energia_liq = EnergiaFioLiquidaREEPMO(np.array([]))
        retas_perdas = RetasPerdasEngolimentoREEPMO(np.array([]))
        risco_ens = RiscoDeficitENSPMO([], np.array([]))
        custo_series = CustoOperacaoPMO(np.array([]))
        valor_esp = CustoOperacaoPMO(np.array([]))
        custo_ref = CustoOperacaoPMO(np.array([]))
        while True:
            # Decide se lê uma linha nova ou usa a última lida
            linha = self._le_linha_com_backup(arq)
            if len(linha) == 0:
                break
            # Condição para finalizar a leitura de um arquivo
            if self._fim_arquivo(linha):
                self.pmo = PMO(ano_pmo,
                               mes_pmo,
                               versao_newave,
                               DadosGeraisPMO(),
                               energia_liq,
                               retas_perdas,
                               EnergiasAfluentesPMO(),
                               EnergiasAfluentesPMO(),
                               EnergiasAfluentesPMO(),
                               {},
                               risco_ens,
                               custo_series,
                               valor_esp,
                               custo_ref)
                break
            # Condição para iniciar uma leitura de dados
            if not achou_dados_pmo and not leu_dados_pmo:
                achou = LeituraPMO.str_dados_pmo in linha
                achou_dados_pmo = achou
            if not achou_efio_liquida:
                achou = LeituraPMO.str_inicio_efio_liquida in linha
                achou_efio_liquida = achou
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
            if achou_efio_liquida:
                energia_liq, retas_perdas = self._le_efio_liquida(arq)
                achou_efio_liquida = False
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
        tabela_energias: np.ndarray = None
        tabela_perdas: np.ndarray = None
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
        linhas_tabela = NUM_ANOS_ESTUDO
        colunas_tabela = 2 * len(SUBMERCADOS)
        tabela = np.zeros((linhas_tabela, colunas_tabela))
        campos_colunas = [5, 7] * len(SUBMERCADOS)
        # Lê a tabela
        for i in range(linhas_tabela):
            linha = self._le_linha_com_backup(arq)
            anos_estudo.append(int(linha[1:5]))
            ci = 7
            for j in range(colunas_tabela):
                cf = ci + campos_colunas[j]
                tabela[i, j] = float(linha[ci:cf])
                ci = cf + 1
        # Constroi o objeto e retorna
        return RiscoDeficitENSPMO(anos_estudo, tabela)

    def _le_tabela_custo(self, arq: IO) -> np.ndarray:
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
