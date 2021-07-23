from inewave.config import SUBMERCADOS, MESES, MESES_DF, MAX_ANOS_ESTUDO
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.registros import RegistroAn, RegistroIn, RegistroFn

from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class BlocoCustoDeficitSistema(Bloco):
    """
    Bloco com informações sobre o custo de déficit por
    patamar de déficit e o número de patamares de déficit.
    """
    str_inicio = " NUMERO DE PATAMARES DE DEFICIT"
    str_fim = " 999"

    def __init__(self):

        super().__init__(BlocoCustoDeficitSistema.str_inicio,
                         "",
                         True)

        self._dados = [0, pd.DataFrame()]

    def __eq__(self, o: object):
        if not isinstance(o, BlocoCustoDeficitSistema):
            return False
        bloco: BlocoCustoDeficitSistema = o
        return all([
                    self._dados[0] == bloco._dados[0],
                    self._dados[1].equals(bloco._dados[1])
                   ])

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            pats = [n for n in range(1, num_pat + 1)]
            cols_custo_pats = [f"Custo Pat. {p}" for p in pats]
            cols_corte_pats = [f"Corte Pat. {p}" for p in pats]
            df.columns = cols_custo_pats + cols_corte_pats
            df["Num. Subsistema"] = num_subsistemas
            df["Nome"] = nomes_subsistemas
            df["Fictício"] = ficticios
            df = df[["Num. Subsistema", "Nome", "Fictício"] +
                    cols_custo_pats +
                    cols_corte_pats]
            return df

        # Variáveis auxiliares
        reg_num = RegistroIn(3)
        reg_nome_subsis = RegistroAn(10)
        reg_flag_ficticio = RegistroIn(1)
        reg_custos = RegistroFn(7)
        reg_pu_corte = RegistroFn(5)
        # Pula a primeira linha, com cabeçalhos
        arq.readline()
        # Lê o número de patamares de déficit
        num_pat = int(reg_num.le_registro(arq.readline(), 1))
        self._dados[0] = num_pat
        # Pula três linhas
        for _ in range(3):
            arq.readline()
        num_subsistemas = []
        nomes_subsistemas = []
        ficticios = []
        tabela = np.zeros((len(SUBMERCADOS) + 1,
                           2 * num_pat))
        for i in range(len(SUBMERCADOS)):
            linha: str = arq.readline()
            num_subsistemas.append(reg_num.le_registro(linha, 1))
            nomes_subsistemas.append(reg_nome_subsis.le_registro(linha, 5))
            ficticios.append(bool(reg_flag_ficticio.le_registro(linha, 17)))
            tabela[i, :num_pat] = reg_custos.le_linha_tabela(linha,
                                                             19,
                                                             1,
                                                             num_pat)
            tabela[i, num_pat:] = reg_pu_corte.le_linha_tabela(linha,
                                                               51,
                                                               1,
                                                               num_pat)
        # Adiciona a linha do fictício
        linha = arq.readline()
        num_subsistemas.append(reg_num.le_registro(linha, 1))
        nomes_subsistemas.append(reg_nome_subsis.le_registro(linha, 5))
        ficticios.append(bool(reg_flag_ficticio.le_registro(linha, 17)))

        self._dados[1] = converte_tabela_em_df()

        # Confirma se terminou
        if BlocoCustoDeficitSistema.str_fim not in arq.readline():
            raise ValueError("Arquivo sistema.dat inválido")

    # Override
    def escreve(self, arq: IO):

        def escreve_custos():
            npat = self._dados[0]
            tabela = self._dados[1]
            lin_tab = tabela.shape[0]
            for i in range(lin_tab):
                linha = ""
                num = tabela.iloc[i, 0]
                nome = tabela.iloc[i, 1]
                fict = int(tabela.iloc[i, 2])
                linha += f" {str(num).ljust(3)}"
                linha += f" {str(nome).ljust(10)}"
                linha += f"  {str(fict)}"
                if num < len(SUBMERCADOS) + 1:
                    for j in range(npat):
                        custo = tabela.iloc[i, j + 3]
                        linha += " " + f"{custo:4.2f}".rjust(7)
                    for j in range(npat):
                        corte = tabela.iloc[i, j + npat + 3]
                        linha += " " + f"{corte:1.3f}".rjust(5)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f"{BlocoCustoDeficitSistema.str_inicio}\n")
        arq.write(" XXX\n")
        arq.write(f" {str(self._dados[0]).rjust(3)}\n")
        arq.write(" CUSTO DO DEFICIT\n")
        arq.write(" NUM|NOME SSIS.|    CUSTO DE DEFICIT POR PATAMAR" +
                  "  | P.U. CORTE POR PATAMAR|\n")
        arq.write(" XXX|XXXXXXXXXX| F|XXXX.XX XXXX.XX XXXX.XX XXXX.XX|" +
                  "X.XXX X.XXX X.XXX X.XXX|\n")
        escreve_custos()
        # Escreve a linha de terminação
        arq.write(f"{BlocoCustoDeficitSistema.str_fim}\n")


class BlocoIntercambioSistema(Bloco):
    """
    Bloco com a informação de intercâmbio
    por mês/ano de estudo para cada subsistema.
    """
    str_inicio = " LIMITES DE INTERCAMBIO"
    str_fim = "999"

    def __init__(self):

        super().__init__(BlocoIntercambioSistema.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoIntercambioSistema):
            return False
        bloco: BlocoIntercambioSistema = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df["De Subsistema"] = subsistemas_de
            df["Para Subsistema"] = subsistemas_para
            df = df[["Ano", "De Subsistema", "Para Subsistema"]
                    + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_ano = RegistroIn(4)
        reg_lim = RegistroFn(7)
        # Pula duas linhas, com cabeçalhos
        arq.readline()
        arq.readline()
        i = 0
        anos = []
        subsistemas_de = []
        subsistemas_para = []
        subsis_de_atual = 0
        subsis_para_atual = 0
        tabela = np.zeros((MAX_ANOS_ESTUDO *
                           2 *
                           len(SUBMERCADOS) ** 2,
                          len(MESES)))
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if BlocoIntercambioSistema.str_fim == linha.strip():
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha
            # Subsistemas de -> para
            if 5 < len(linha.strip()) < 30:
                subsis_de_atual = int(linha[1:4].strip())
                subsis_para_atual = int(linha[5:8].strip())
                continue
            elif len(linha.strip()) < 5:
                subsis_para_atual, subsis_de_atual = (subsis_de_atual,
                                                      subsis_para_atual)
            else:
                subsistemas_de.append(subsis_de_atual)
                subsistemas_para.append(subsis_para_atual)
                # Ano
                anos.append(reg_ano.le_registro(linha, 0))
                # Limites
                tabela[i, :] = reg_lim.le_linha_tabela(linha,
                                                       7,
                                                       1,
                                                       len(MESES))
                i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_limites():
            lin_tab = self._dados.shape[0]
            subsistema_de_anterior = 0
            subsistema_para_anterior = 0
            for i in range(lin_tab):
                linha = ""
                # Subsistemas de / para
                subsistema_de = self._dados.iloc[i, 1]
                subsistema_para = self._dados.iloc[i, 2]
                if any([
                        subsistema_de != subsistema_de_anterior,
                        subsistema_para != subsistema_para_anterior
                       ]):
                    if not all([
                                subsistema_de == subsistema_para_anterior,
                                subsistema_para == subsistema_de_anterior
                               ]):
                        linha = (str(subsistema_de).rjust(4) +
                                 str(subsistema_para).rjust(4) +
                                 "               0")
                    arq.write(linha + "\n")
                    subsistema_de_anterior = subsistema_de
                    subsistema_para_anterior = subsistema_para

                # Patamares de cada mês
                linha = f"{self._dados.iloc[i, 0]}   "
                for j in range(len(MESES)):
                    v = self._dados.iloc[i, j + 3]
                    linha += " {:6.0f}".format(v).rjust(7)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f"{BlocoIntercambioSistema.str_inicio}\n")
        arq.write(" A   B   A->B    B->A\n")
        cab = (" XXX XXX XJAN. XXXFEV. XXXMAR. XXXABR. XXXMAI." +
               " XXXJUN. XXXJUL. XXXAGO. XXXSET. XXXOUT. XXXNOV. XXXDEZ.\n")
        arq.write(cab)
        escreve_limites()
        # Escreve a linha de terminação
        arq.write(f" {BlocoIntercambioSistema.str_fim}\n")


class BlocoMercadoEnergiaSistema(Bloco):
    """
    Bloco com a informação de mercado de energia
    por mês/ano de estudo para cada subsistema.
    """
    str_inicio = " MERCADO DE ENERGIA TOTAL"
    str_fim = "999"

    def __init__(self):

        super().__init__(BlocoMercadoEnergiaSistema.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoMercadoEnergiaSistema):
            return False
        bloco: BlocoMercadoEnergiaSistema = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df["Subsistema"] = subsistema
            df = df[["Ano", "Subsistema"] + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_subsis = RegistroIn(3)
        reg_ano = RegistroAn(4)
        reg_merc = RegistroFn(7)
        # Pula duas linhas, com cabeçalhos
        arq.readline()
        arq.readline()
        i = 0
        anos = []
        subsistema = []
        subsistema_atual = 0
        tabela = np.zeros((MAX_ANOS_ESTUDO * len(SUBMERCADOS),
                          len(MESES)))
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if BlocoMercadoEnergiaSistema.str_fim == linha.strip():
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha
            if len(linha.strip()) < 5:
                subsistema_atual = reg_subsis.le_registro(linha, 1)
            else:
                # Ano
                anos.append(reg_ano.le_registro(linha, 0))
                # Subsistema
                subsistema.append(subsistema_atual)
                # Limites
                tabela[i, :] = reg_merc.le_linha_tabela(linha,
                                                        7,
                                                        1,
                                                        len(MESES))
                i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_mercados():
            lin_tab = self._dados.shape[0]
            subsistema_anterior = 0
            for i in range(lin_tab):
                linha = ""
                # Subsistema
                subsistema = self._dados.iloc[i, 1]
                if subsistema != subsistema_anterior:
                    arq.write(" " + str(subsistema).rjust(3) + "\n")
                    subsistema_anterior = subsistema
                # Mercados de cada mês
                linha = f"{self._dados.iloc[i, 0].ljust(4)}   "
                for j in range(len(MESES)):
                    v = self._dados.iloc[i, j + 2]
                    linha += " {:6.0f}".format(v).rjust(7)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f"{BlocoMercadoEnergiaSistema.str_inicio}\n")
        arq.write(" XXX\n")
        cab = ("       XXXJAN. XXXFEV. XXXMAR. XXXABR. XXXMAI. XXXJUN." +
               " XXXJUL. XXXAGO. XXXSET. XXXOUT. XXXNOV. XXXDEZ.\n")
        arq.write(cab)
        escreve_mercados()
        # Escreve a linha de terminação
        arq.write(f" {BlocoMercadoEnergiaSistema.str_fim}\n")


class BlocoGeracaoUsinasNaoSimuladasSistema(Bloco):
    """
    Bloco com a informação de geração das usinas não simuladas
    por mês/ano de estudo para cada subsistema.
    """
    str_inicio = " GERACAO DE USINAS NAO SIMULADAS"
    str_fim = "999"

    def __init__(self):

        super().__init__(BlocoGeracaoUsinasNaoSimuladasSistema.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoGeracaoUsinasNaoSimuladasSistema):
            return False
        bloco: BlocoGeracaoUsinasNaoSimuladasSistema = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df["Subsistema"] = subsistema
            df = df[["Ano", "Subsistema"] + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_subsis = RegistroIn(3)
        reg_ano = RegistroIn(4)
        reg_ger = RegistroFn(7)
        # Pula duas linhas, com cabeçalhos
        arq.readline()
        arq.readline()
        i = 0
        anos = []
        subsistema = []
        subsistema_atual = 0
        tabela = np.zeros((MAX_ANOS_ESTUDO * len(SUBMERCADOS),
                          len(MESES)))
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if BlocoGeracaoUsinasNaoSimuladasSistema.str_fim == linha.strip():
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha
            if len(linha.strip()) < 5:
                subsistema_atual = reg_subsis.le_registro(linha, 1)
            else:
                # Ano
                anos.append(reg_ano.le_registro(linha, 0))
                # Subsistema
                subsistema.append(subsistema_atual)
                # Limites
                tabela[i, :] = reg_ger.le_linha_tabela(linha,
                                                       7,
                                                       1,
                                                       len(MESES))
                i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_geracoes():
            lin_tab = self._dados.shape[0]
            subsistema_anterior = 0
            for i in range(lin_tab):
                linha = ""
                # Subsistema
                subsistema = self._dados.iloc[i, 1]
                if subsistema != subsistema_anterior:
                    arq.write(" " + str(subsistema).rjust(3) + "\n")
                    subsistema_anterior = subsistema
                # Mercados de cada mês
                linha = f"{str(self._dados.iloc[i, 0]).ljust(4)}   "
                for j in range(len(MESES)):
                    v = self._dados.iloc[i, j + 2]
                    linha += " {:6.0f}".format(v).rjust(7)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f"{BlocoGeracaoUsinasNaoSimuladasSistema.str_inicio}\n")
        arq.write(" XXX  XBL  XXXXXXXXXXXXXXXXXXXX  XTE\n")
        cab = ("       XXXJAN. XXXFEV. XXXMAR. XXXABR. XXXMAI. XXXJUN." +
               " XXXJUL. XXXAGO. XXXSET. XXXOUT. XXXNOV. XXXDEZ.\n")
        arq.write(cab)
        escreve_geracoes()
        # Escreve a linha de terminação
        arq.write(f" {BlocoGeracaoUsinasNaoSimuladasSistema.str_fim}\n")


class LeituraSistema(Leitura):
    """
    Realiza a leitura do arquivo `sistema.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `sistema.dat`, construindo
    um objeto `Sistema` cujas informações são as mesmas do sistema.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self,
                 diretorio: str):
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo sistema.dat.
        """
        return [BlocoCustoDeficitSistema(),
                BlocoIntercambioSistema(),
                BlocoMercadoEnergiaSistema(),
                BlocoGeracaoUsinasNaoSimuladasSistema()]
