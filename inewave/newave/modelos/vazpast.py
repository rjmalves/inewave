# Imports do próprio módulo
from inewave._utils.registros import RegistroAn, RegistroFn, RegistroIn
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave.config import MAX_UHES, MESES, MESES_DF
# Imports de módulos externos
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import IO, List


class BlocoVazPast(Bloco):
    """
    Bloco de informações de vazões passadas
    por usina, existentes no arquivo `vazpast.dat`
    do NEWAVE.
    """
    str_inicio = ""

    def __init__(self):

        super().__init__(BlocoVazPast.str_inicio,
                         "",
                         True)

        self._dados = [0, 0, pd.DataFrame]

    def __eq__(self, o: object):
        if not isinstance(o, BlocoVazPast):
            return False
        bloco: BlocoVazPast = o
        return all([
                    self._dados[0] == bloco._dados[0],
                    self._dados[1] == bloco._dados[1],
                    self._dados[2].equals(bloco._dados[2])
                   ])

    # Override
    def le(self, arq: IO):
        # Pula as duas primeiras linhas, com cabeçalhos
        arq.readline()
        # Extrai o mês e ano do estudo
        linha = arq.readline()

        str_mes_plan, str_ano_plan = linha.split("ANOPLAN")
        self._dados[0] = int(str_mes_plan.split("=")[1].strip())
        self._dados[1] = int(str_ano_plan.split("=")[1].strip())
        # Variáveis auxiliares
        reg_posto = RegistroIn(3)
        reg_nome = RegistroAn(12)
        reg_vaz = RegistroFn(8)
        i = 0
        postos: List[int] = []
        nomes: List[str] = []
        tabela = np.zeros((MAX_UHES, len(MESES)))
        while True:
            # Verifica se o arquivo acabou
            linha = arq.readline()
            if len(linha) < 3:
                tabela = tabela[:i, :]
                self._dados[2] = pd.DataFrame(tabela)
                self._dados[2].columns = MESES_DF
                self._dados[2]["Posto"] = postos
                self._dados[2]["Usina"] = nomes
                self._dados[2] = self._dados[2][["Posto", "Usina"] + MESES_DF]
                break
            # Senão, lê mais uma linha
            postos.append(reg_posto.le_registro(linha, 2))
            nomes.append(reg_nome.le_registro(linha, 6))
            tabela[i, :] = reg_vaz.le_linha_tabela(linha,
                                                   20,
                                                   2,
                                                   len(MESES))
            i += 1

    # Override
    def escreve(self, arq: IO):

        def escreve_desvios():
            lin_tab = self._dados[2].shape[0]
            for i in range(lin_tab):
                linha = " "
                # Posto
                linha += str(self._dados[2].iloc[i, 0]).rjust(4) + " "
                # Nome
                linha += str(self._dados[2].iloc[i, 1]).ljust(12)
                # Vazoes de cada mês
                for j in range(len(MESES)):
                    v = self._dados[2].iloc[i, 2 + j]
                    linha += " " + "{:6.2f}".format(float(v)).rjust(9)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        dummy = ("********* DUMMY" + "\n")
        arq.write(dummy)
        arq.write(dummy)
        ano_mes = " "
        ano_mes += f"MESPLAN={str(self._dados[0]).rjust(13)}"
        ano_mes += f"  ANOPLAN={str(self._dados[1]).rjust(13)}"
        arq.write(ano_mes + "\n")
        escreve_desvios()


class LeituraVazPast(Leitura):
    """
    Realiza a leitura do arquivo `vazpast.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `vazpast.dat`, construindo
    um objeto `VazPast` cujas informações são as mesmas do `vazpast.dat`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    def _cria_blocos_leitura(self) -> List[Bloco]:
        return [BlocoVazPast()]
