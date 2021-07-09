# Imports do próprio módulo
from inewave.config import MAX_ITERS, REES
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
# Imports de módulos externos
import numpy as np  # type: ignore
from typing import IO, List


class RegistroNwlistcf:
    """
    Armazena as informações de um registro da FCF do NEWAVE.

    ** Parâmetros **

    - ireg: `int`
    - rhs:  `float`
    - tabela: `np.ndarray`

    """

    __slots__ = ["ireg",
                 "rhs",
                 "tabela"]

    def __init__(self,
                 ireg: int,
                 rhs: float,
                 tabela: np.ndarray):
        self.ireg = ireg
        self.rhs = rhs
        self.tabela = tabela

    @classmethod
    def le_registro(cls, primeira_linha: str, arq: IO) -> 'RegistroNwlistcf':
        """
        """
        primeira = True
        n_rees = len(REES)
        n_cols_tabela = 16
        ireg = 0
        rhs = 0.0
        tabela = np.zeros((n_rees, n_cols_tabela))
        for i in range(n_rees):
            if primeira:
                primeira = False
                linha = primeira_linha
                # Extrai os campos específicos da primeira linha
                ireg = int(linha[2:10])
                rhs = float(linha[15:30])
            # Preenche a tabela com os dados do registro
            else:
                linha = arq.readline()
            ree = int(linha[11:14])
            ci = 31
            nc = 17
            for j in range(n_cols_tabela):
                cf = ci + nc
                num_str = linha[ci:cf]
                valor = 0.0 if not num_str.isnumeric() else float(num_str)
                tabela[ree-1, j] = valor
                ci = cf + 1

        return cls(ireg, rhs, tabela)

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre RegistroNwlistcf avalia todos os
        valores.
        """
        if not isinstance(o, RegistroNwlistcf):
            return False
        reg: RegistroNwlistcf = o
        eq_ireg = self.ireg == reg.ireg
        eq_rhs = self.rhs == reg.rhs
        eq_tab = np.array_equal(self.tabela, reg.tabela)

        return all([eq_ireg,
                    eq_rhs,
                    eq_tab])


class BlocoPeriodoNwlistcf(Bloco):
    """
    Bloco com informações dos cortes de um período,
    existentes no arquivo `nwlistcf.rel` do NWLISTCF.
    """
    str_inicio = "  PERIODO:  "

    def __init__(self):

        super().__init__(BlocoPeriodoNwlistcf.str_inicio,
                         "",
                         False)

        self._dados: List[RegistroNwlistcf] = []

    def __eq__(self, o: object):
        if not isinstance(o, BlocoPeriodoNwlistcf):
            return False
        bloco: BlocoPeriodoNwlistcf = o
        return all([d1 == d2
                    for d1, d2 in zip(self._dados, bloco._dados)])

    # Override
    def le(self, arq: IO):
        # Salta duas linhas para acessar a tabela
        arq.readline()
        arq.readline()
        while True:
            # Verifica se a próxima linha é o início do
            # próximo período ou é vazia
            linha = arq.readline()
            if (BlocoPeriodoNwlistcf.str_inicio in linha
                    or len(linha) < 2):
                break
            # Senão, lê mais um registro
            reg = RegistroNwlistcf.le_registro(linha, arq)
            self._dados.append(reg)

        return linha

    # Override
    def escreve(self, arq: IO):
        pass


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

    """
    str_inicio_periodo = "  PERIODO:      "

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    def _cria_blocos_leitura(self) -> List[Bloco]:
        return [BlocoPeriodoNwlistcf()
                for _ in range(MAX_ITERS)]
