from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave._utils.registros import RegistroAn, RegistroIn, RegistroFn
from inewave.config import MAX_LAG_ADTERM, MAX_UTES, NUM_PATAMARES

from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class BlocoUTEsAdTerm(Bloco):
    """
    Bloco com os despachos antecipados das UTEs por patamar.
    """
    str_inicio = ""
    str_fim = "9999"

    def __init__(self):

        super().__init__(BlocoUTEsAdTerm.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoUTEsAdTerm):
            return False
        bloco: BlocoUTEsAdTerm = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            pats = [n for n in range(1, NUM_PATAMARES + 1)]
            cols_pats = [f"Patamar {p}" for p in pats]
            df.columns = cols_pats
            df["Índice UTE"] = iutes
            df["Nome"] = nomes_utes
            df["Lag"] = lags_utes
            df = df[["Índice UTE", "Nome", "Lag"] + cols_pats]
            return df

        # Variáveis auxiliares
        reg_iute = RegistroIn(4)
        reg_nome = RegistroAn(12)
        reg_despacho = RegistroFn(10)
        # Pula as duas primeiras linhas, com cabeçalhos
        arq.readline()
        i = 0
        iutes = []
        nomes_utes = []
        lags_utes = []
        iute_atual = 0
        nome_ute_atual = ""
        lag_leitura = 1
        tabela = np.zeros((MAX_UTES * MAX_LAG_ADTERM,
                           NUM_PATAMARES))
        while True:
            # Verifica se o arquivo acabou
            linha: str = arq.readline()
            if BlocoUTEsAdTerm.str_fim in linha:
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha
            # Ano
            if linha[1:5].strip().isnumeric():
                iute_atual = reg_iute.le_registro(linha, 1)
                nome_ute_atual = reg_nome.le_registro(linha, 7)
                lag_leitura = 1
            else:
                iutes.append(iute_atual)
                nomes_utes.append(nome_ute_atual)
                lags_utes.append(lag_leitura)
                # Patamares
                tabela[i, :] = reg_despacho.le_linha_tabela(linha,
                                                            24,
                                                            2,
                                                            NUM_PATAMARES)
                lag_leitura += 1
                i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_termicas():
            tabela = self._dados
            lin_tab = tabela.shape[0]
            for i in range(lin_tab):
                iute = tabela.iloc[i, 0]
                nome = tabela.iloc[i, 1]
                lag = tabela.iloc[i, 2]
                if lag == 1:
                    # Descobre o número de lags da UTE
                    lag_ute = tabela.loc[tabela["Índice UTE"] == iute,
                                         "Índice UTE"].shape[0]
                    linha_ute = (f" {str(iute).rjust(4)}  " +
                                 f"{str(nome).ljust(12)}  {lag_ute}")
                    arq.write(linha_ute + "\n")

                # Despachos
                linha = "                      "
                despachos = len([c for c in list(self._dados.columns)
                                 if "Patamar" in c])
                for j in range(despachos):
                    v = tabela.iloc[i, j + 3]
                    linha += "  " + "{:7.2f}".format(v).rjust(10)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        titulos = " IUTE  NOME TERMICA LAG" + "\n"
        cab = (" XXXX  XXXXXXXXXXXX  X  XXXXXXX.XX" +
               "  XXXXXXX.XX  XXXXXXX.XX" + "\n")
        arq.write(titulos)
        arq.write(cab)
        escreve_termicas()
        # Escreve a linha de terminação
        arq.write(f" {BlocoUTEsAdTerm.str_fim}\n")


class LeituraAdTerm(Leitura):
    """
    Realiza a leitura do arquivo `adterm.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `adterm.dat`, construindo
    um objeto `AdTerm` cujas informações são as mesmas do adterm.dat.

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
        Cria a lista de blocos a serem lidos no arquivo adterm.dat.
        """
        return [BlocoUTEsAdTerm()]
