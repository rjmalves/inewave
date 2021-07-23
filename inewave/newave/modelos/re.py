from inewave.config import MAX_RES
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.registros import RegistroFn, RegistroIn

from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class BlocoUsinasConjuntoRE(Bloco):
    """
    Bloco com informações das usinas pertencentes a cada conjunto
    de restrições elétricas por conjunto de RE.
    """
    str_inicio = "RES   USINAS PERTENCENTES AO CONJUNTO"
    str_fim = "999"

    def __init__(self):

        super().__init__(BlocoUsinasConjuntoRE.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoUsinasConjuntoRE):
            return False
        bloco: BlocoUsinasConjuntoRE = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            cols_usinas = [f"Usina {i}" for i in range(1, 11)]
            df.columns = cols_usinas
            df["Conjunto"] = conjuntos
            df = df[["Conjunto"] + cols_usinas]
            return df

        # Variáveis auxiliares
        reg_conjunto = RegistroIn(3)
        # Pula uma linha, com cabeçalhos
        arq.readline()
        i = 0
        conjuntos = []
        tabela = np.zeros((MAX_RES, 10), dtype=np.int64)
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if (BlocoUsinasConjuntoRE.str_fim
               == linha.strip()):
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            conjuntos.append(reg_conjunto.le_registro(linha, 0))
            col_i = 6
            # Lê a linha conferindo quantas colunas tem
            linha_tabela: List[int] = []
            for j in range(1, 11):
                col_f = col_i + 3
                if col_f >= len(linha):
                    break
                linha_tabela.append(int(linha[col_i:col_f]))
                col_i = col_f + 1
            for j, usi in enumerate(linha_tabela):
                tabela[i, j] = usi
            i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_conjuntos():
            lin_tab = self._dados.shape[0]
            for i in range(lin_tab):
                linha = f"{str(int(self._dados.iloc[i, 0])).rjust(3)}  "
                for j in range(1, 11):
                    usi = self._dados.iloc[i, j]
                    if usi == 0:
                        continue
                    linha += f" {str(self._dados.iloc[i, j]).rjust(3)}"
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f"{BlocoUsinasConjuntoRE.str_inicio}\n")
        arq.write("XXX   XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX\n")
        escreve_conjuntos()
        # Escreve a linha de terminação
        arq.write(f"{BlocoUsinasConjuntoRE.str_fim}\n")


class BlocoConfiguracaoRestricoesRE(Bloco):
    """
    Bloco com informações de configuração das restrições elétricas
    para cada conjunto de usinas.
    """
    str_inicio = "RES MM/AAAA MM/AAAA P       RESTRICAO"
    str_fim = "999"

    def __init__(self):

        super().__init__(BlocoConfiguracaoRestricoesRE.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoConfiguracaoRestricoesRE):
            return False
        bloco: BlocoConfiguracaoRestricoesRE = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = ["Conjunto", "Mês Início", "Ano Início",
                          "Mês Fim", "Ano Fim", "Flag P"]
            df["Restrição"] = restricoes
            df["Motivo"] = motivos
            return df

        # Variáveis auxiliares
        reg_conjunto = RegistroIn(3)
        reg_mes = RegistroIn(2)
        reg_ano = RegistroIn(4)
        reg_flag = RegistroIn(1)
        reg_resticao = RegistroFn(15)
        # Pula uma linha, com cabeçalhos
        arq.readline()
        i = 0
        tabela = np.zeros((MAX_RES, 6), dtype=np.int64)
        restricoes = []
        motivos = []
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if (BlocoUsinasConjuntoRE.str_fim
               == linha.strip()):
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            tabela[i, 0] = reg_conjunto.le_registro(linha, 0)
            tabela[i, 1] = reg_mes.le_registro(linha, 4)
            tabela[i, 2] = reg_ano.le_registro(linha, 7)
            tabela[i, 3] = reg_mes.le_registro(linha, 12)
            tabela[i, 4] = reg_ano.le_registro(linha, 15)
            tabela[i, 5] = reg_flag.le_registro(linha, 20)
            restricoes.append(reg_resticao.le_registro(linha, 22))
            motivos.append(linha[38:].strip())
            i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_restricoes():
            lin_tab = self._dados.shape[0]
            for i in range(lin_tab):
                linha = f"{str(int(self._dados.iloc[i, 0])).rjust(3)}"
                linha += f" {str(int(self._dados.iloc[i, 1])).rjust(2)}"
                linha += f" {str(int(self._dados.iloc[i, 2])).rjust(4)}"
                linha += f" {str(int(self._dados.iloc[i, 3])).rjust(2)}"
                linha += f" {str(int(self._dados.iloc[i, 4])).rjust(4)}"
                linha += f" {str(int(self._dados.iloc[i, 5]))}"
                linha += " " + f"{self._dados.iloc[i, 6]:12.2f}".rjust(15)
                linha += f" {self._dados.iloc[i, 7]}"
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f"{BlocoConfiguracaoRestricoesRE.str_inicio}\n")
        arq.write("XXX XX XXXX XX XXXX X XXXXXXXXXXXXXXX\n")
        escreve_restricoes()
        # Escreve a linha de terminação
        arq.write(f"{BlocoConfiguracaoRestricoesRE.str_fim}\n")


class LeituraRE(Leitura):
    """
    Realiza a leitura do arquivo `re.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `re.dat`, construindo
    um objeto `RE` cujas informações são as mesmas do re.dat.

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
        Cria a lista de blocos a serem lidos no arquivo re.dat.
        """
        return [BlocoUsinasConjuntoRE(),
                BlocoConfiguracaoRestricoesRE()]
