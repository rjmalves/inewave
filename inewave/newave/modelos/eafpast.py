# Imports do próprio módulo
from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave.config import MAX_UHES, MESES, MESES_DF
# Imports de módulos externos
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import IO, List


class BlocoEafPast(Bloco):
    """
    Bloco de informações de vazões passadas
    por REE, existentes no arquivo `eafpast.dat`
    do NEWAVE.
    """
    str_inicio = ""

    def __init__(self):

        super().__init__(BlocoEafPast.str_inicio,
                         "",
                         True)

        self._dados = pd.DataFrame

    def __eq__(self, o: object):
        if not isinstance(o, BlocoEafPast):
            return False
        bloco: BlocoEafPast = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):
        # Pula as duas primeiras linhas, com cabeçalhos
        arq.readline()

        # Variáveis auxiliares
        reg_num = RegistroIn(4)
        reg_nome = RegistroAn(10)
        reg_vaz = RegistroFn(8)
        i = 0
        nums: List[int] = []
        nomes: List[str] = []
        tabela = np.zeros((MAX_UHES, len(MESES)))
        while True:
            # Verifica se o arquivo acabou
            linha = arq.readline()
            if len(linha) < 3:
                tabela = tabela[:i, :]
                self._dados = pd.DataFrame(tabela)
                self._dados.columns = MESES_DF
                self._dados["Índice"] = nums
                self._dados["REE"] = nomes
                self._dados = self._dados[["Índice", "REE"] + MESES_DF]
                break
            # Senão, lê mais uma linha
            nums.append(reg_num.le_registro(linha, 0))
            nomes.append(reg_nome.le_registro(linha, 5))
            tabela[i, :] = reg_vaz.le_linha_tabela(linha,
                                                   18,
                                                   3,
                                                   len(MESES))
            i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_afluencias():
            lin_tab = self._dados.shape[0]
            for i in range(lin_tab):
                linha = ""
                # Numero
                linha += str(self._dados.iloc[i, 0]).rjust(4) + " "
                # REE
                linha += str(self._dados.iloc[i, 1]).ljust(10)
                # Vazoes de cada mês
                for j in range(len(MESES)):
                    v = self._dados.iloc[i, 2 + j]
                    linha += "   " + "{:5.2f}".format(float(v)).rjust(8)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        cabs = (" NUM SISTEMA        JAN        FEV        MAR        ABR" +
                "        MAI        JUN        JUL        AGO        SET " +
                "       OUT        NOV        DEZ" + "\n")
        tabs = ("XXXX XXXXXXXXXX   XXXXX.XX   XXXXX.XX   XXXXX.XX   XXXXX." +
                "XX   XXXXX.XX   XXXXX.XX   XXXXX.XX   XXXXX.XX   XXXXX.XX" +
                "   XXXXX.XX   XXXXX.XX   XXXXX.XX" + "\n")
        arq.write(cabs)
        arq.write(tabs)
        escreve_afluencias()


class LeituraEafPast(Leitura):
    """
    Realiza a leitura do arquivo `eafpast.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `rafpast.dat`, construindo
    um objeto `EafPast` cujas informações são as mesmas do `eafpast.dat`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    def _cria_blocos_leitura(self) -> List[Bloco]:
        return [BlocoEafPast()]
