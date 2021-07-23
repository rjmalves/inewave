from inewave.config import SUBMERCADOS, MESES, MESES_DF, MAX_ANOS_ESTUDO
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.registros import RegistroAn, RegistroIn, RegistroFn

from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class BlocoCargasAdicionaisSubsistema(Bloco):
    """
    Bloco com informações de cargas adicionais por mês/ano
    e por subsistema.
    """
    str_inicio = ""
    str_fim = "999"

    def __init__(self):

        super().__init__(BlocoCargasAdicionaisSubsistema.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoCargasAdicionaisSubsistema):
            return False
        bloco: BlocoCargasAdicionaisSubsistema = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df["Num. Subsistema"] = subsistema
            df["Nome Subsistema"] = nome_subsistema
            df["Razão Carga"] = razao_carga
            df = df[["Ano", "Num. Subsistema",
                     "Nome Subsistema", "Razão Carga"] + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_subsis = RegistroIn(3)
        reg_nome_subsis = RegistroAn(12)
        reg_razao_carga = RegistroAn(12)
        reg_ano = RegistroAn(4)
        reg_carga = RegistroFn(7)
        # Pula uma linha, com cabeçalhos
        arq.readline()
        i = 0
        anos = []
        subsistema = []
        nome_subsistema = []
        subsistema_atual = 0
        nome_subsistema_atual = ""
        razao_carga = []
        razao_carga_atual = ""
        tabela = np.zeros((MAX_ANOS_ESTUDO * len(SUBMERCADOS),
                          len(MESES)))
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if BlocoCargasAdicionaisSubsistema.str_fim == linha.strip():
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha
            if len(linha.strip()) < 40:
                subsistema_atual = reg_subsis.le_registro(linha, 1)
                nome_subsistema_atual = reg_nome_subsis.le_registro(linha, 6)
                razao_carga_atual = reg_razao_carga.le_registro(linha, 20)
            else:
                # Ano
                anos.append(reg_ano.le_registro(linha, 0))
                # Subsistema
                subsistema.append(subsistema_atual)
                nome_subsistema.append(nome_subsistema_atual)
                razao_carga.append(razao_carga_atual)
                # Limites
                tabela[i, :] = reg_carga.le_linha_tabela(linha,
                                                         7,
                                                         1,
                                                         len(MESES))
                i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_cargas():
            lin_tab = self._dados.shape[0]
            subsistema_anterior = 0
            nome_anterior = ""
            razao_anterior = ""
            for i in range(lin_tab):
                linha = ""
                # Subsistema
                subsistema = self._dados.iloc[i, 1]
                nome = self._dados.iloc[i, 2]
                razao = self._dados.iloc[i, 3]
                if any([
                        subsistema != subsistema_anterior,
                        nome != nome_anterior,
                        razao != razao_anterior
                       ]):
                    subsistema_anterior = subsistema
                    nome_anterior = nome
                    razao_anterior = razao
                    linha = (" " + str(subsistema).rjust(3) +
                             "  " + str(nome).ljust(12) +
                             "  " + str(razao).ljust(12))
                    arq.write(linha + "\n")
                    subsistema_anterior = subsistema
                # Mercados de cada mês
                linha = f"{self._dados.iloc[i, 0].ljust(4)}   "
                for j in range(len(MESES)):
                    v = self._dados.iloc[i, j + 4]
                    linha += " {:6.0f}".format(v).rjust(7)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(" XXX\n")
        cab = ("       XXXJAN. XXXFEV. XXXMAR. XXXABR. XXXMAI. XXXJUN." +
               " XXXJUL. XXXAGO. XXXSET. XXXOUT. XXXNOV. XXXDEZ.\n")
        arq.write(cab)
        escreve_cargas()
        # Escreve a linha de terminação
        arq.write(f" {BlocoCargasAdicionaisSubsistema.str_fim}\n")


class LeituraCAdic(Leitura):
    """
    Realiza a leitura do arquivo `cadic.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `cadic.dat`, construindo
    um objeto `CAdic` cujas informações são as mesmas do cadic.dat.

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
        Cria a lista de blocos a serem lidos no arquivo cadic.dat.
        """
        return [BlocoCargasAdicionaisSubsistema()]
