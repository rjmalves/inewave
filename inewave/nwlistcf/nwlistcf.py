# Imports do próprio módulo
from inewave.config import REES
from inewave._utils.leitura import Leitura
from .modelos.nwlistcf import Nwlistcf, RegistroNwlistcf
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from traceback import print_exc
from typing import IO, Dict


class LeituraNwlistcf(Leitura):
    """
    Realiza a leitura do arquivo nwlistcf.rel,
    existente em um diretório de saídas do NWLISTCF.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos do arquivo nwlistcf.rel, construindo um
    objeto `Nwlistcf` cujas informações são as mesmas do arquivo.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `nwlistcf`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraNwlistcf(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> nwlist= leitor.nwlist

    """
    str_inicio_periodo = "  PERIODO:      "

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        self.nwlistcf = Nwlistcf({})

    def le_arquivo(self) -> Nwlistcf:
        """
        Faz a leitura do arquivo `nwlistcf.rel`.
        """
        try:
            achou = False
            caminho = os.path.join(self.diretorio, "nwlistcf.rel")
            with open(caminho, "r") as arq:
                while True:
                    linha = self._le_linha_com_backup(arq)
                    # Verifica se o arquivo acabou
                    if achou and len(linha) < 2:
                        break
                    # Verifica se a próxima linha indica um novo período
                    if LeituraNwlistcf.str_inicio_periodo in linha:
                        achou = True
                        periodo = int(linha[12:].strip())
                        p = self._le_periodo(arq)
                        self.nwlistcf.registros[periodo] = p
                return self.nwlistcf
        except Exception:
            print_exc()
            return self.nwlistcf

    def _le_periodo(self, arq: IO) -> Dict[int, RegistroNwlistcf]:
        """
        Lê um período do arquivo nwlistcf.rel.
        """
        # Salta duas linhas para acessar a tabela
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        p: Dict[int, RegistroNwlistcf] = {}
        while True:
            # Verifica se a próxima linha é o início do
            # próximo período ou é vazia
            linha = self._le_linha_com_backup(arq)
            if (LeituraNwlistcf.str_inicio_periodo in linha
                    or len(linha) < 2):
                break
            # Senão, lê mais um registro
            self._configura_backup()
            reg = self._le_registro(arq)
            p[reg.ireg] = reg

        return p

    def _le_registro(self, arq: IO) -> RegistroNwlistcf:
        """
        """
        primeira_linha = True
        n_rees = len(REES)
        n_cols_tabela = 16
        ireg = 0
        rhs = 0.0
        tabela = np.zeros((n_rees, n_cols_tabela))
        for i in range(n_rees):
            linha = self._le_linha_com_backup(arq)
            if primeira_linha:
                primeira_linha = False
                # Extrai os campos específicos da primeira linha
                ireg = int(linha[2:10])
                rhs = float(linha[15:30])
            # Preenche a tabela com os dados do registro
            ree = int(linha[11:14])
            ci = 31
            nc = 17
            for j in range(n_cols_tabela):
                cf = ci + nc
                num_str = linha[ci:cf]
                valor = 0.0 if not num_str.isnumeric() else float(num_str)
                tabela[ree-1, j] = valor
                ci = cf + 1

        return RegistroNwlistcf(ireg,
                                rhs,
                                tabela)

    def _fim_arquivo(self, linha: str) -> bool:
        return super()._fim_arquivo(linha)
