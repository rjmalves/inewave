# Imports do próprio módulo
from inewave._utils.escrita import Escrita
from inewave._utils.leitura import Leitura
from .modelos.vazpast import VazPast
from inewave.config import MESES
# Imports de módulos externos
import os
import numpy as np  # type: ignore
from traceback import print_exc
from typing import IO, List


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

    Uma vez realizada a leitura do arquivo, as informações são guardadas
    internamente no atributo `vazpast`.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> leitor = LeituraVazPast(diretorio)
    >>> leitor.le_arquivo()
    # Ops, esqueci de pegar o objeto
    >>> vazpast = leitor.vazpast

    """

    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # Confhd default, depois é substituído
        self.vazpast = VazPast(0, 0, [], [], np.array([]))

    def le_arquivo(self) -> VazPast:
        """
        Faz a leitura do arquivo `vazpast.dat`.
        """
        try:
            caminho = os.path.join(self.diretorio, "vazpast.dat")
            with open(caminho, "r") as arq:
                self.confhd = self._le_vazpast(arq)
                return self.vazpast
        except Exception:
            print_exc()
            return self.vazpast

    def _le_vazpast(self, arq: IO) -> VazPast:
        """
        Faz a leitura do arquivo vazpast.dat.
        """
        # Pula as duas primeiras linhas, com cabeçalhos
        self._le_linha_com_backup(arq)
        self._le_linha_com_backup(arq)
        n_meses = len(MESES)
        # Extrai o mês e ano do estudo
        linha = self._le_linha_com_backup(arq)
        str_mes_plan, str_ano_plan = linha.split("ANOPLAN")
        mes_plan = int(str_mes_plan[9:].strip())
        ano_plan = int(str_ano_plan[9:].strip())
        # Lê as informações da tabela
        postos: List[int] = []
        nomes: List[str] = []
        tabela = np.zeros((5000, n_meses))
        i = 0
        while True:
            # Verifica se o arquivo acabou
            linha = self._le_linha_com_backup(arq)
            if self._fim_arquivo(linha):
                self.vazpast = VazPast(mes_plan,
                                       ano_plan,
                                       postos,
                                       nomes,
                                       tabela[:i, :])
                break
            # Senão, lê mais uma linha
            # Posto
            postos.append(int(linha[:5]))
            # Nome
            nomes.append(linha[6:18].strip())
            # Vazoes passadas de cada mês
            ci = 19
            nc = 9
            for m in range(n_meses):
                cf = ci + nc
                valor = float(linha[ci:cf])
                tabela[i, m] = valor
                ci = cf + 1
            i += 1

        return self.vazpast

    def _fim_arquivo(self, linha: str) -> bool:
        return len(linha) < 1


class EscritaVazPast(Escrita):
    """
    Realiza a escrita do arquivo vazpast.dat
    em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para escrever os campos
    de um arquivo vazpast.dat, a partir de um objeto `VazPast`.

    Este objeto existe para retirar do modelo de dados a complexidade
    de armazenar as strings auxiliares do arquivo, desenhar tabelas, dentre
    outras tarefas associadas à escrita.

    Se o diretório de escrita não existir, ele será criado.

    **Exemplos**

    >>> diretorio = "~/documentos/.../deck"
    >>> # vaz é do tipo VazPast
    >>> escritor = EscritaVazPast(diretorio)
    >>> escritor.escreve_arquivo(vaz)
    """
    def __init__(self, diretorio: str):
        super().__init__()
        self.diretorio = diretorio

    def escreve_arquivo(self, vazpast: VazPast):
        """
        Realiza a escrita de um arquivo `vazpast.dat`.
        """
        # Confere se o diretório existe. Senão, cria.
        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)
        # Inicia a escrita
        caminho = os.path.join(self.diretorio, "vazpast.dat")
        n_meses = len(MESES)
        with open(caminho, "w") as arq:

            def escreve_desvios(vaz: VazPast):
                lin_tab = vaz.tabela.shape[0]
                for i in range(lin_tab):
                    linha = " "
                    # Posto
                    linha += str(vaz.postos[i]).rjust(4) + " "
                    # Nome
                    linha += str(vaz.nomes[i]).ljust(12)
                    # Vazoes de cada mês
                    for j in range(n_meses):
                        v = vaz.tabela[i, j]
                        linha += " " + "{:6.2f}".format(v).rjust(9)
                    arq.write(linha + "\n")

            # Escreve cabeçalhos
            dummy = ("********* DUMMY" + "\n")
            arq.write(dummy)
            arq.write(dummy)
            ano_mes = " "
            ano_mes += f"MESPLAN={str(vazpast.mes_planejamento).rjust(13)}"
            ano_mes += f"  ANOPLAN={str(vazpast.ano_planejamento).rjust(13)}"
            arq.write(ano_mes + "\n")
            escreve_desvios(vazpast)
