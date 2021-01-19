# Imports do próprio módulo
from inewave._utils.leitura import Leitura
from inewave.config import NUM_ANOS_ESTUDO, NUM_PATAMARES, MESES
from .modelos.patamar import Patamar
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from traceback import print_exc
from typing import IO, List, Tuple


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

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `patamar`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraPatamar(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> patamar = leitor.patamar

    """
    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # Patamar default, depois é substituído
        self.patamar = Patamar(0, [], np.array([]))

    def le_arquivo(self) -> Patamar:
        """
        Realiza a leitura do arquivo `patamar.dat`.
        """
        try:
            caminho = os.path.join(self.diretorio, "patamar.dat")
            with open(caminho, "r") as arq:
                # Pula inicialmente duas linhas
                # de número de patamares
                self._le_linha_com_backup(arq)
                self._le_linha_com_backup(arq)
                # A terceira linha tem o número de patamares
                linha = self._le_linha_com_backup(arq)
                num_pat = int(linha[1:3])
                if num_pat != NUM_PATAMARES:
                    raise Exception("Número de patamares incompatível")
                # Em seguida, pula três linhas e inicia a leitura
                # da tabela de patamares
                self._le_linha_com_backup(arq)
                self._le_linha_com_backup(arq)
                self._le_linha_com_backup(arq)
                # Lê a tabela de valores
                anos, tabela = self._le_patamares(arq)
                self.patamar = Patamar(NUM_PATAMARES, anos, tabela)
                return self.patamar
        except Exception:
            print_exc()
            return Patamar(0, [], np.array([]))

    def _le_patamares(self, arq: IO) -> Tuple[List[int], np.ndarray]:
        """
        Faz a leitura da tabela de patamares de carga.
        """
        anos: List[int] = []
        patamares = np.zeros((NUM_PATAMARES * NUM_ANOS_ESTUDO,
                              len(MESES)))
        for n in range(NUM_ANOS_ESTUDO):
            a, p = self._le_patamares_ano(arq)
            anos.append(a)
            li = n * NUM_PATAMARES
            lf = li + NUM_PATAMARES
            patamares[li:lf, :] = p
        return anos, patamares

    def _le_patamares_ano(self, arq: IO) -> Tuple[int, np.ndarray]:
        """
        Lê os patamares de um ano na tabela de patamares.
        """
        patamares_ano = np.zeros((NUM_PATAMARES, len(MESES)))
        cols = 6
        ano = 0
        for p in range(NUM_PATAMARES):
            linha = self._le_linha_com_backup(arq)
            if p == 0:
                # Se é o primeiro patamar, extrai o ano
                ano = int(linha[0:4])
            col_i = 6
            for m in range(len(MESES)):
                col_f = col_i + cols
                patamares_ano[p, m] = float(linha[col_i:col_f])
                col_i = col_f + 2
        return ano, patamares_ano

    def _fim_arquivo(self, linha: str) -> bool:
        return False
