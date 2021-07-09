# Imports do próprio módulo
from inewave._utils.registros import RegistroFn, RegistroIn
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave.config import MAX_ANOS_ESTUDO, MAX_UHES, MESES
# Imports de módulos externos
import numpy as np  # type: ignore
from typing import IO, List


class BlocoDsvUHE(Bloco):
    """
    Bloco de informações do desvio de água por
    usina no arquivo do NEWAVE `dsvagua.dat`.
    """
    str_inicio = ""

    def __init__(self):

        super().__init__(BlocoDsvUHE.str_inicio,
                         "",
                         True)

        self._dados: np.ndarray = np.zeros((MAX_ANOS_ESTUDO * MAX_UHES,
                                           len(MESES) + 3),
                                           dtype=np.float64)

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre EnergiaFioLiquidaREEPMO avalia todos os campos.
        """
        if not isinstance(o, BlocoDsvUHE):
            return False
        e: BlocoDsvUHE = o
        return np.array_equal(self._dados, e._dados)

    # Override
    def le(self, arq: IO):
        # Variáveis auxiliares
        reg_ano = RegistroIn(4)
        reg_usi = RegistroIn(3)
        reg_dsv = RegistroFn(6)
        reg_flag = RegistroIn(1)
        # Pula a linha com cabeçalhos
        arq.readline()
        i = 0
        while True:
            # Verifica se o arquivo acabou
            linha = arq.readline()
            if linha.strip() == "9999":
                self._dados = self._dados[:i, :]
                break
            # Senão, lê mais uma linha
            # Ano
            self._dados[i, 0] = reg_ano.le_registro(linha, 0)
            # Usina
            self._dados[i, 1] = reg_usi.le_registro(linha, 6)
            # Desvios
            self._dados[i, 2:-1] = reg_dsv.le_linha_tabela(linha,
                                                           10,
                                                           1,
                                                           len(MESES))
            # Flag
            self._dados[i, -1] = reg_flag.le_registro(linha, 97)
            i += 1

    # Override
    def escreve(self, arq: IO):
        n_meses = len(MESES)

        def escreve_desvios():
            lin_tab = self._dados.shape[0]
            for i in range(lin_tab):
                linha = ""
                # Ano
                linha += str(int(self._dados[i, 0])).rjust(4) + "  "
                # Usina
                linha += str(int(self._dados[i, 1])).rjust(3) + " "
                # Desvios de cada mês
                for j in range(n_meses):
                    v = self._dados[i, j + 2]
                    linha += "{:3.2f}".format(v).rjust(6) + " "
                # Flag de usar desvio
                linha += str(int(self._dados[i, -1])).rjust(4)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        titulos = ("ANO  USIN    JAN    FEV    MAR    ABR    MAI    JUN"
                   + "    JUL    AGO    SET    OUT    NOV    DEZ" + "\n")
        cab = ("XXXX  XXX XXXX.X XXXX.X XXXX.X XXXX.X XXXX.X XXXX.X "
               + "XXXX.X XXXX.X XXXX.X XXXX.X XXXX.X XXXX.X" + "\n")
        arq.write(titulos)
        arq.write(cab)
        escreve_desvios()
        # Escreve a linha de terminação
        arq.write("9999\n")


class LeituraDSVAgua(Leitura):
    """
    Realiza a leitura do arquivo `dsvagua.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `dsvagua.dat`, construindo
    um objeto `DSVAgua` cujas informações são as mesmas do `dsvagua.dat`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    def _cria_blocos_leitura(self) -> List[Bloco]:
        return [BlocoDsvUHE()]
