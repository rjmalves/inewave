from inewave._utils.bloco import Bloco
from inewave._utils.leitura import Leitura
from inewave.config import MAX_ANOS_ESTUDO, MESES_DF
from inewave._utils.registros import RegistroAn, RegistroFn  # typer: ignore

from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class BlocoValoresConstantesCVAR(Bloco):
    """
    Bloco com valores dos parâmetros ALFA e LAMBDA constantes.
    """
    str_inicio = "VALORES CONSTANTE NO TEMPO"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoValoresConstantesCVAR.str_inicio,
                         "",
                         True)

        self._dados: List[float] = []

    def __eq__(self, o: object):
        if not isinstance(o, BlocoValoresConstantesCVAR):
            return False
        bloco: BlocoValoresConstantesCVAR = o
        return self._dados == bloco._dados

    # Override
    def le(self, arq: IO):
        # Variáveis auxiliares
        reg_cvar = RegistroFn(5)
        # Pula uma linha, com cabeçalhos
        arq.readline()
        # Lê os parâmetros:
        linha = arq.readline()
        self._dados = reg_cvar.le_linha_tabela(linha, 7, 2, 2)

    # Override
    def escreve(self, arq: IO):
        # Escreve cabeçalhos
        arq.write(f"{BlocoValoresConstantesCVAR.str_inicio}\n")
        arq.write("       ALF.x  LBD.x\n")
        arq.write("       " +
                  f"{round(self._dados[0], 1)}".rjust(5) +
                  "  " +
                  f"{round(self._dados[1], 1)}".rjust(5) +
                  "\n")


class BlocoAlfaVariavelCVAR(Bloco):
    """
    Bloco com informações do parâmetro ALFA variável no tempo.
    """
    str_inicio = "VALORES DE ALFA VARIAVEIS NO TEMPO"
    str_fim = "VALORES DE LAMBDA VARIAVEIS NO TEMPO"

    def __init__(self):

        super().__init__(BlocoAlfaVariavelCVAR.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoAlfaVariavelCVAR):
            return False
        bloco: BlocoAlfaVariavelCVAR = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df = df[["Ano"] + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_ano = RegistroAn(5)
        reg_tabela = RegistroFn(5)
        i = 0
        anos = []
        tabela = np.zeros((MAX_ANOS_ESTUDO,
                          len(MESES_DF)))
        # Pula uma linha, com cabeçalhos
        arq.readline()
        while True:
            # Verifica se o bloco acabou
            linha: str = arq.readline()
            if BlocoAlfaVariavelCVAR.str_fim == linha.strip():
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha

            # Ano
            anos.append(reg_ano.le_registro(linha, 0))
            # Tabela
            tabela[i, :] = reg_tabela.le_linha_tabela(linha,
                                                      7,
                                                      2,
                                                      len(MESES_DF))
            i += 1
        return linha

    # Override
    def escreve(self, arq: IO):

        def escreve_tabela():
            for _, lin in self._dados.iterrows():
                linha = ""
                if str(lin["Ano"]).isnumeric():
                    linha += str(lin["Ano"]).rjust(5)
                else:
                    linha += str(lin["Ano"]).ljust(5)
                # Tabela
                for m in MESES_DF:
                    linha += "  " + f"{round(float(lin[m]), 1)}".rjust(5)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f"{BlocoAlfaVariavelCVAR.str_inicio}\n")
        arq.write("       JAN.X  FEV.X  MAR.X  ABR.X  MAI.X  JUN.X" +
                  "  JUL.X  AGO.X  SET.X  OUT.X  NOV.X  DEZ.X\n")
        escreve_tabela()


class BlocoLambdaVariavelCVAR(Bloco):
    """
    Bloco com informações do parâmetro LAMBDA variável no tempo.
    """
    str_inicio = "VALORES DE LAMBDA VARIAVEIS NO TEMPO"
    str_fim = ""

    def __init__(self):

        super().__init__(BlocoLambdaVariavelCVAR.str_inicio,
                         "",
                         True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoLambdaVariavelCVAR):
            return False
        bloco: BlocoLambdaVariavelCVAR = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):

        def converte_tabela_em_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            df.columns = MESES_DF
            df["Ano"] = anos
            df = df[["Ano"] + MESES_DF]
            return df

        # Variáveis auxiliares
        reg_ano = RegistroAn(5)
        reg_tabela = RegistroFn(5)
        i = 0
        anos = []
        tabela = np.zeros((MAX_ANOS_ESTUDO,
                          len(MESES_DF)))
        # Pula uma linha, com cabeçalhos
        arq.readline()
        while True:
            # Verifica se o bloco acabou
            linha: str = arq.readline()
            if len(linha) < 5:
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            # Senão, lê mais uma linha

            # Ano
            anos.append(reg_ano.le_registro(linha, 0))
            # Tabela
            tabela[i, :] = reg_tabela.le_linha_tabela(linha,
                                                      7,
                                                      2,
                                                      len(MESES_DF))
            i += 1
        return linha

    # Override
    def escreve(self, arq: IO):

        def escreve_tabela():
            for _, lin in self._dados.iterrows():
                linha = ""
                if str(lin["Ano"]).isnumeric():
                    linha += str(lin["Ano"]).rjust(5)
                else:
                    linha += str(lin["Ano"]).ljust(5)
                # Tabela
                for m in MESES_DF:
                    linha += "  " + f"{round(float(lin[m]), 1)}".rjust(5)
                arq.write(linha + "\n")

        # Escreve cabeçalhos
        arq.write(f"{BlocoLambdaVariavelCVAR.str_inicio}\n")
        arq.write("       JAN.X  FEV.X  MAR.X  ABR.X  MAI.X  JUN.X" +
                  "  JUL.X  AGO.X  SET.X  OUT.X  NOV.X  DEZ.X\n")
        escreve_tabela()


class LeituraCVAR(Leitura):
    """
    Realiza a leitura do arquivo `cvar.dat`
    existente em um diretório de entradas do NEWAVE.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo `cvar.dat`, construindo
    um objeto `CVAR` cujas informações são as mesmas do cvar.dat.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.
    """

    def __init__(self,
                 diretorio: str):
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo cvar.dat.
        """
        return [BlocoValoresConstantesCVAR(),
                BlocoAlfaVariavelCVAR(),
                BlocoLambdaVariavelCVAR()]
