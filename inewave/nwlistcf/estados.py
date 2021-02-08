# Imports do próprio módulo
from inewave.config import REES
from inewave._utils.leitura import Leitura
from .modelos.estados import Estados, RegistroEstado
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from traceback import print_exc
from typing import IO, Dict


class LeituraEstados(Leitura):
    """
    Realiza a leitura do arquivo estados.rel,
    existente em um diretório de saídas do NWLISTCF.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos do arquivo estados.rel, construindo um
    objeto `Estados` cujas informações são as mesmas do arquivo.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `estados`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraEstados(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> estados = leitor.estados

    """
    str_inicio_periodo = "  PERIODO:      "

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        self.estados = Estados({})

    def le_arquivo(self) -> Estados:
        """
        Faz a leitura do arquivo `estados.rel`.
        """
        try:
            caminho = os.path.join(self.diretorio, "estados.rel")
            with open(caminho, "r") as arq:
                while True:
                    linha = self._le_linha_com_backup(arq)
                    # Verifica se o arquivo acabou
                    if len(linha) < 2:
                        break
                    # Verifica se a próxima linha indica um novo período
                    if LeituraEstados.str_inicio_periodo in linha:
                        periodo = int(linha[12:].strip())
                        p = self._le_periodo(arq)
                        self.estados.registros[periodo] = p
                return self.estados
        except Exception:
            print_exc()
            return self.estados

    def _le_periodo(self, arq: IO) -> Dict[int, RegistroEstado]:
        """
        Lê um período do arquivo estados.rel.
        """
        # Salta duas linhas para acessar a tabela
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        p: Dict[int, RegistroEstado] = {}
        while True:
            # Verifica se a próxima linha é o início do
            # próximo período ou é vazia
            linha = self._le_linha_com_backup(arq)
            if (LeituraEstados.str_inicio_periodo in linha
                    or len(linha) < 2):
                break
            # Senão, lê mais um registro
            self._configura_backup()
            reg = self._le_registro(arq)
            p[reg.ireg] = reg

        return p

    def _le_registro(self, arq: IO) -> RegistroEstado:
        """
        """
        primeira_linha = True
        n_rees = len(REES)
        n_cols_tabela = 18
        ireg = 0
        itec = 0
        simc = 0
        itef = 0
        fobj = 0.
        tabela = np.zeros((n_rees, n_cols_tabela))
        for i in range(n_rees):
            linha = self._le_linha_com_backup(arq)
            if primeira_linha:
                primeira_linha = False
                # Extrai os campos específicos da primeira linha
                ireg = int(linha[2:10])
                itec = int(linha[11:15])
                simc = int(linha[16:20])
                itef = int(linha[21:25])
                fobj = float(linha[31:48])
            # Preenche a tabela com os dados do registro
            ree = int(linha[26:30])
            ci = 49
            nc = 17
            for j in range(n_cols_tabela):
                cf = ci + nc
                num_str = linha[ci:cf]
                valor = 0.0 if not num_str.isnumeric() else float(num_str)
                tabela[ree-1, j] = valor
                ci = cf + 1

        return RegistroEstado(ireg,
                              itec,
                              simc,
                              itef,
                              fobj,
                              tabela)

    def _fim_arquivo(self, linha: str) -> bool:
        return super()._fim_arquivo(linha)
