# Imports do próprio módulo
from inewave._utils.registros import RegistroFn, RegistroIn
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave.config import MAX_ANOS_ESTUDO, MESES
# Imports de módulos externos
import numpy as np  # type: ignore
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

        self._dados: np.ndarray = np.zeros((3 * MAX_ANOS_ESTUDO,
                                           len(MESES) + 1),
                                           dtype=np.float64)

    # Override
    def le(self, arq: IO):
        # Variáveis auxiliares
        reg_ano = RegistroIn(4)
        reg_pat = RegistroFn(6)
        # Pula as duas primeiras linhas, com cabeçalhos
        arq.readline()
        arq.readline()
        i = 0
        while True:
            # Verifica se o arquivo acabou
            linha = arq.readline()
            if BlocoDuracaoPatamar.str_fim in linha:
                self._dados = self._dados[:i, :]
                break
            # Senão, lê mais uma linha
            # Ano
            if linha[0:4].isnumeric():
                self._dados[i, 0] = reg_ano.le_registro(linha, 0)
            # Desvios
            self._dados[i, 1:] = reg_pat.le_linha_tabela(linha,
                                                         6,
                                                         2,
                                                         len(MESES))
            i += 1

    # Override
    def escreve(self, arq: IO):
        n_meses = len(MESES)

        def escreve_patamares():
            lin_tab = self._dados.shape[0]
            for i in range(lin_tab):
                linha = ""
                # Ano
                if int(self._dados[i, 0]) != 0:
                    linha += str(int(self._dados[i, 0])).rjust(4) + "  "
                else:
                    linha += "      "
                # Patamares de cada mês
                for j in range(n_meses):
                    v = self._dados[i, j + 1]
                    linha += "{:1.4f}".format(v).rjust(6) + "  "
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
        return [BlocoDuracaoPatamar()]
