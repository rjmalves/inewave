# Imports do próprio módulo
from inewave._utils.escrita import Escrita
from inewave._utils.leitura import Leitura
from .modelos.dsvagua import DSVAgua
from inewave.config import MESES
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from traceback import print_exc
from typing import IO


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

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `dsvagua`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraDSVAgua(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> dsv = leitor.dsvagua

    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # Confhd default, depois é substituído
        self.dsvagua = DSVAgua(np.array([]))

    def le_arquivo(self) -> DSVAgua:
        """
        Faz a leitura do arquivo `dsvagua.dat`.
        """
        try:
            caminho = os.path.join(self.diretorio, "dsvagua.dat")
            with open(caminho, "r") as arq:
                self.confhd = self._le_dsvagua(arq)
                return self.dsvagua
        except Exception:
            print_exc()
            return self.dsvagua

    def _le_dsvagua(self, arq: IO) -> DSVAgua:
        """
        Faz a leitura do arquivo dsvagua.dat.
        """
        linha = ""
        # Pula as duas primeiras linhas, com cabeçalhos
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        n_meses = len(MESES)
        tabela = np.zeros((5000, n_meses + 3))
        i = 0
        while True:
            # Verifica se o arquivo acabou
            linha = self._le_linha_com_backup(arq)
            if self._fim_arquivo(linha):
                self.dsvagua = DSVAgua(tabela[:i, :])
                break
            # Senão, lê mais uma linha
            # Ano
            tabela[i, 0] = int(linha[:4])
            # Usina
            tabela[i, 1] = int(linha[6:9])
            # Desvios de cada mês
            ci = 10
            nc = 6
            for m in range(n_meses):
                cf = ci + nc
                valor = float(linha[ci:cf])
                tabela[i, m + 2] = valor
                ci = cf + 1
            tabela[i, -1] = int(linha[97])
            i += 1

        return self.dsvagua

    def _fim_arquivo(self, linha: str) -> bool:
        return linha.strip() == "9999"


class EscritaDSVAgua(Escrita):
    """
    Realiza a escrita do arquivo dsvagua.dat
    em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para escrever os campos
    de um arquivo dsvagua.dat, a partir de um objeto `DSVAgua`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de armazenar as strings auxiliares do arquivo, desenhar tabelas, dentre
    outras tarefas associadas à escrita.

    Se o diretório de escrita não existir, ele será criado.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> # dsv é do tipo DSVAgua
    >>> escritor = EscritaDSVAgua(diretorio)
    >>> escritor.escreve_arquivo(dsv)
    """
    def __init__(self, diretorio: str):
        super().__init__()
        self.diretorio = diretorio

    def escreve_arquivo(self, dsvagua: DSVAgua):
        """
        Realiza a escrita de um arquivo `dsvagua.dat`.
        """
        # Confere se o diretório existe. Senão, cria.
        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)
        # Inicia a escrita
        caminho = os.path.join(self.diretorio, "dsvagua.dat")
        n_meses = len(MESES)
        with open(caminho, "w") as arq:

            def escreve_desvios(dsv: DSVAgua):
                lin_tab = dsv.tabela.shape[0]
                for i in range(lin_tab):
                    linha = ""
                    # Ano
                    linha += str(int(dsv.tabela[i, 0])).rjust(4) + "  "
                    # Usina
                    linha += str(int(dsv.tabela[i, 1])).rjust(3) + " "
                    # Desvios de cada mês
                    for j in range(n_meses):
                        v = dsv.tabela[i, j + 2]
                        linha += "{:4.2f}".format(v).rjust(6) + " "
                    # Flag de usar desvio
                    linha += str(int(dsv.tabela[i, -1])).rjust(4)
                    arq.write(linha + "\n")

            # Escreve cabeçalhos
            titulos = ("ANO  USIN    JAN    FEV    MAR    ABR    MAI    JUN"
                       + "    JUL    AGO    SET    OUT    NOV    DEZ" + "\n")
            cab = ("XXXX  XXX XXXX.X XXXX.X XXXX.X XXXX.X XXXX.X XXXX.X "
                   + "XXXX.X XXXX.X XXXX.X XXXX.X XXXX.X XXXX.X" + "\n")
            arq.write(titulos)
            arq.write(cab)
            escreve_desvios(dsvagua)
            # Escreve a linha de terminação
            arq.write("9999\n")
