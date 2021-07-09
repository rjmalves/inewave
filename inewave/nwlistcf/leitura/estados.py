# Imports do próprio módulo
from inewave.config import MAX_ITERS, REES
from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
# Imports de módulos externos
import numpy as np  # type: ignore
from typing import IO, List


class RegistroEstado:
    """
    Armazena as informações de um registro visitado pelo NEWAVE
    em algum período de alguma simulação.

    ** Parâmetros **

    - ireg: `int`
    - itec: `int`
    - simc: `int`
    - itef: `int`
    - fobj: `int`
    - tabela: `np.ndarray`

    """

    __slots__ = ["ireg",
                 "itec",
                 "simc",
                 "itef",
                 "fobj",
                 "tabela"]

    def __init__(self,
                 ireg: int,
                 itec: int,
                 simc: int,
                 itef: int,
                 fobj: float,
                 tabela: np.ndarray):
        self.ireg = ireg
        self.itec = itec
        self.simc = simc
        self.itef = itef
        self.fobj = fobj
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre RegistroEstado avalia todos os
        valores.
        """
        if not isinstance(o, RegistroEstado):
            return False
        reg: RegistroEstado = o
        eq_ireg = self.ireg == reg.ireg
        eq_itec = self.itec == reg.itec
        eq_simc = self.simc == reg.simc
        eq_itef = self.itef == reg.itef
        eq_fobj = self.fobj == reg.fobj
        eq_tab = np.array_equal(self.tabela, reg.tabela)

        return all([eq_ireg,
                    eq_itec,
                    eq_simc,
                    eq_itef,
                    eq_fobj,
                    eq_tab])

    @classmethod
    def le_registro(cls, primeira_linha: str, arq: IO) -> 'RegistroEstado':
        """
        """
        primeira = True
        n_rees = len(REES)
        n_cols_tabela = 18
        ireg = 0
        itec = 0
        simc = 0
        itef = 0
        fobj = 0.
        tabela = np.zeros((n_rees, n_cols_tabela))
        for i in range(n_rees):
            if primeira:
                primeira = False
                linha = primeira_linha
                # Extrai os campos específicos da primeira linha
                ireg = int(linha[2:10])
                itec = int(linha[11:15])
                simc = int(linha[16:20])
                itef = int(linha[21:25])
                fobj = float(linha[31:48])
            else:
                linha = arq.readline()
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

        return cls(ireg,
                   itec,
                   simc,
                   itef,
                   fobj,
                   tabela)


class BlocoRegistroEstados(Bloco):
    """
    Bloco com informações do estado de construção dos cortes
    de um período, existentes no arquivo `estados.rel` do NWLISTCF.
    """
    str_inicio = "  PERIODO:  "

    def __init__(self):

        super().__init__(BlocoRegistroEstados.str_inicio,
                         "",
                         False)

        self._dados: List[RegistroEstado] = []

    def __eq__(self, o: object):
        if not isinstance(o, BlocoRegistroEstados):
            return False
        bloco: BlocoRegistroEstados = o
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
            if (BlocoRegistroEstados.str_inicio in linha
                    or len(linha) < 2):
                break
            # Senão, lê mais um registro
            reg = RegistroEstado.le_registro(linha, arq)
            self._dados.append(reg)

        return linha

    # Override
    def escreve(self, arq: IO):
        pass


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

    """
    str_inicio_periodo = "  PERIODO:   "

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__(diretorio)

    def _cria_blocos_leitura(self) -> List[Bloco]:
        return [BlocoRegistroEstados()
                for _ in range(MAX_ITERS)]
