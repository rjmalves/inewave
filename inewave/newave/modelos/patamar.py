# Imports do próprio módulo
from inewave._utils.registros import RegistroFn, RegistroIn
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave.config import MAX_ANOS_ESTUDO
from inewave.config import MESES
from inewave.config import MESES_DF
from inewave.config import NUM_PATAMARES
from inewave.config import SUBMERCADOS

# Imports de módulos externos
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import IO, List


class BlocoDuracaoPatamar(Bloco):
    """
    Bloco com a duração de cada patamar por mês
    de estudo, extraído do arquivo `patamar.dat`.
    """
    str_inicio = "ANO   DURACAO MENSAL DOS PATAMARES DE CARGA"
    str_fim = "SUBSISTEMA"

    def __init__(self):

        super().__init__(BlocoDuracaoPatamar.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoDuracaoPatamar):
            return False
        bloco: BlocoDuracaoPatamar = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            pats = [n for n in range(1, NUM_PATAMARES + 1)]
            coluna_pats = pats * int(i / NUM_PATAMARES)
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df["Patamar"] = coluna_pats
            df = df[["Ano", "Patamar"] + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_ano = RegistroIn(4)
        reg_pat = RegistroFn(6)
        # Pula as duas primeiras linhas, com cabeçalhos
        arq.readline()
        arq.readline()
        i = 0
        anos = []
        tabela = np.zeros((MAX_ANOS_ESTUDO * NUM_PATAMARES,
                          len(MESES)))
        while True:
            # Verifica se o arquivo acabou
            linha = arq.readline()
            if BlocoDuracaoPatamar.str_fim in linha:
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha
            # Ano
            if linha[0:4].isnumeric():
                anos.append(reg_ano.le_registro(linha, 0))
            else:
                anos.append(anos[-1])
            # Patamares
            tabela[i, :] = reg_pat.le_linha_tabela(linha,
                                                   6,
                                                   2,
                                                   len(MESES))
            i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_patamares():
            lin_tab = self._dados.shape[0]
            for i in range(lin_tab):
                linha = ""
                # Ano
                if i % NUM_PATAMARES == 0:
                    linha += str(int(self._dados.iloc[i, 0])).rjust(4)
                else:
                    linha += "    "
                # Patamares de cada mês
                for j in range(len(MESES)):
                    v = self._dados.iloc[i, j + 2]
                    linha += "{:1.4f}".format(v).rjust(8)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        titulos = ("      JAN     FEV     MAR     ABR     MAI     JUN     "
                   + "JUL     AGO     SET     OUT     NOV     DEZ" + "\n")
        cab = ("      X.XXXX  X.XXXX  X.XXXX  X.XXXX  X.XXXX  X.XXXX  "
               + "X.XXXX  X.XXXX  X.XXXX  X.XXXX  X.XXXX  X.XXXX" + "\n")
        arq.write(f"{BlocoDuracaoPatamar.str_inicio}\n")
        arq.write(titulos)
        arq.write(cab)
        escreve_patamares()
        # Escreve a linha de terminação
        arq.write(f" {BlocoDuracaoPatamar.str_fim}\n")


class BlocoCargaPatamarSubsistemas(Bloco):
    """
    Bloco com a informação de carga (em p.u.) por patamar de carga
    e por mês/ano de estudo para cada subsistema.
    """
    str_inicio = "    ANO                       CARGA(P.U.DEMANDA MED.)"
    str_fim = "9999"

    def __init__(self):

        super().__init__(BlocoCargaPatamarSubsistemas.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoCargaPatamarSubsistemas):
            return False
        bloco: BlocoCargaPatamarSubsistemas = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            pats = [n for n in range(1, NUM_PATAMARES + 1)]
            coluna_pats = pats * int(i / NUM_PATAMARES)
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df["Patamar"] = coluna_pats
            df["Subsistema"] = subsistemas
            df = df[["Ano", "Patamar", "Subsistema"] + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_ano = RegistroIn(4)
        reg_pat = RegistroFn(6)
        # Pula as duas primeiras linhas, com cabeçalhos
        arq.readline()
        i = 0
        anos = []
        subsistemas = []
        subsistema_atual = 0
        tabela = np.zeros((MAX_ANOS_ESTUDO * NUM_PATAMARES * len(SUBMERCADOS),
                          len(MESES)))
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if BlocoCargaPatamarSubsistemas.str_fim == linha.strip():
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha
            # Subsistema
            if linha.strip().isnumeric():
                subsistema_atual = int(linha)
                continue
            subsistemas.append(subsistema_atual)
            # Ano
            if linha[3:7].isnumeric():
                anos.append(reg_ano.le_registro(linha, 3))
            else:
                anos.append(anos[-1])
            # Patamares
            tabela[i, :] = reg_pat.le_linha_tabela(linha,
                                                   8,
                                                   1,
                                                   len(MESES))
            i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_patamares():
            lin_tab = self._dados.shape[0]
            subsistema_anterior = 0
            i_subsistema = 0
            for i in range(lin_tab):
                linha = ""
                # Subsistema
                subsistema = self._dados.iloc[i, 2]
                if subsistema != subsistema_anterior:
                    linha += str(subsistema).rjust(4)
                    subsistema_anterior = subsistema
                    i_subsistema = 0
                else:
                    # Ano
                    if i_subsistema % NUM_PATAMARES == 0:
                        linha += "   " + str(self._dados.iloc[i, 0]).rjust(4)
                    else:
                        linha += "       "
                    i_subsistema += 1
                    # Patamares de cada mês
                    for j in range(len(MESES)):
                        v = self._dados.iloc[i, j + 3]
                        linha += "{:1.4f}".format(v).rjust(7)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        cab = ("   XXXX X.XXXX X.XXXX X.XXXX X.XXXX X.XXXX X.XXXX"
               + " X.XXXX X.XXXX X.XXXX X.XXXX X.XXXX X.XXXX" + "\n")
        arq.write(f"{BlocoCargaPatamarSubsistemas.str_inicio}\n")
        arq.write(cab)
        escreve_patamares()
        # Escreve a linha de terminação
        arq.write(f" {BlocoCargaPatamarSubsistemas.str_fim}\n")


class BlocoIntercambioPatamarSubsistemas(Bloco):
    """
    Bloco com a informação de intercâmbio (em p.u.) por patamar de carga
    e por mês/ano de estudo para cada subsistema.
    """
    str_inicio = "                             INTERCAMBIO(P.U.INTERC.MEDIO)"
    str_fim = "9999"

    def __init__(self):

        super().__init__(BlocoIntercambioPatamarSubsistemas.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoIntercambioPatamarSubsistemas):
            return False
        bloco: BlocoIntercambioPatamarSubsistemas = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            pats = [n for n in range(1, NUM_PATAMARES + 1)]
            coluna_pats = pats * int(i / NUM_PATAMARES)
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df["Patamar"] = coluna_pats
            df["De Subsistema"] = subsistemas_de
            df["Para Subsistema"] = subsistemas_para
            df = df[["Ano", "Patamar", "De Subsistema", "Para Subsistema"]
                    + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_ano = RegistroIn(4)
        reg_pat = RegistroFn(6)
        # Pula a primeira linha, com cabeçalhos
        arq.readline()
        i = 0
        anos = []
        subsistemas_de = []
        subsistemas_para = []
        subsistema_de_atual = 0
        subsistema_para_atual = 0
        tabela = np.zeros((MAX_ANOS_ESTUDO *
                           NUM_PATAMARES *
                           len(SUBMERCADOS) ** 2,
                          len(MESES)))
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if BlocoIntercambioPatamarSubsistemas.str_fim == linha.strip():
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha
            # Subsistemas de -> para
            if len(linha) < 12:
                subsistema_de_atual = int(linha[1:4].strip())
                subsistema_para_atual = int(linha[5:8].strip())
                continue
            subsistemas_de.append(subsistema_de_atual)
            subsistemas_para.append(subsistema_para_atual)
            # Ano
            if linha[3:7].isnumeric():
                anos.append(reg_ano.le_registro(linha, 3))
            else:
                anos.append(anos[-1])
            # Patamares
            tabela[i, :] = reg_pat.le_linha_tabela(linha,
                                                   8,
                                                   1,
                                                   len(MESES))
            i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_patamares():
            lin_tab = self._dados.shape[0]
            subsistema_de_anterior = 0
            subsistema_para_anterior = 0
            i_subsistema = 0
            for i in range(lin_tab):
                linha = ""
                # Subsistemas de / para
                subsistema_de = self._dados.iloc[i, 2]
                subsistema_para = self._dados.iloc[i, 3]
                if any([
                        subsistema_de != subsistema_de_anterior,
                        subsistema_para != subsistema_para_anterior
                       ]):
                    linha = (str(subsistema_de).rjust(4) +
                             str(subsistema_para).rjust(4))
                    subsistema_de_anterior = subsistema_de
                    subsistema_para_anterior = subsistema_para
                    i_subsistema = 0
                else:
                    # Ano
                    if i_subsistema % NUM_PATAMARES == 0:
                        linha += "   " + str(self._dados.iloc[i, 0]).rjust(4)
                    else:
                        linha += "       "
                    i_subsistema += 1
                    # Patamares de cada mês
                    for j in range(len(MESES)):
                        v = self._dados.iloc[i, j + 4]
                        linha += "{:1.4f}".format(v).rjust(7)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        cab = ("   XXXX X.XXXX X.XXXX X.XXXX X.XXXX X.XXXX X.XXXX"
               + " X.XXXX X.XXXX X.XXXX X.XXXX X.XXXX X.XXXX" + "\n")
        arq.write(f"{BlocoIntercambioPatamarSubsistemas.str_inicio}\n")
        arq.write(cab)
        escreve_patamares()
        # Escreve a linha de terminação
        arq.write(f" {BlocoIntercambioPatamarSubsistemas.str_fim}\n")


class LeituraPatamar(Leitura):
    """
    Realiza a leitura do arquivo patamar.dat
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo patamar.dat, construindo
    um objeto `Patamar` cujas informações são as mesmas do patamar.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        return [BlocoDuracaoPatamar(),
                BlocoCargaPatamarSubsistemas(),
                BlocoIntercambioPatamarSubsistemas()]
