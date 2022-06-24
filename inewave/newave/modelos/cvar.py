from inewave.config import MAX_ANOS_ESTUDO, MESES_DF

from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.floatfield import FloatField
from cfinterface.components.literalfield import LiteralField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class BlocoValoresConstantesCVAR(Block):
    """
    Bloco com valores dos parâmetros ALFA e LAMBDA constantes.
    """

    BEGIN_PATTERN = "VALORES CONSTANTE NO TEMPO"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                FloatField(5, 7, 1),
                FloatField(5, 14, 1),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoValoresConstantesCVAR):
            return False
        bloco: BlocoValoresConstantesCVAR = o
        if not all(
            [
                isinstance(self.data, list),
                isinstance(o.data, list),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO):
        for _ in range(2):
            self.__cabecalhos.append(file.readline())
        self.data = self.__linha.read(file.readline())

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, list):
            raise ValueError("Dados do cvar.dat não foram lidos com sucesso")
        file.write(self.__linha.write(self.data))


class BlocoAlfaVariavelNoTempo(Block):
    """
    Bloco com a informação do valor de ALFA por estágio
    no horizonte de execução.
    """

    BEGIN_PATTERN = "VALORES DE ALFA VARIAVEIS NO TEMPO"
    END_PATTERN = "VALORES DE LAMBDA VARIAVEIS NO TEMPO"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_ano: List[Field] = [LiteralField(5, 0)]
        campos_valores: List[Field] = [
            FloatField(5, 7 * i + 7, 1) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_valores)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoAlfaVariavelNoTempo):
            return False
        bloco: BlocoAlfaVariavelNoTempo = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=MESES_DF)
            df["Ano"] = anos
            df = df
            df = df[["Ano"] + MESES_DF]
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_ANOS_ESTUDO, len(MESES_DF)))
        anos: List[str] = []
        while True:
            ultima_linha = file.tell()
            linha = file.readline()
            if len(linha) < 3:
                break
            # Confere se terminaram
            if self.ends(linha):
                file.seek(ultima_linha)
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            anos.append(dados[0])
            tabela[i, :] = dados[1:]
            i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do cvar.dat não foram lidos com sucesso")

        for _, lin in self.data.iterrows():
            file.write(self.__linha.write(lin.tolist()))


class BlocoLambdaVariavelNoTempo(Block):
    """
    Bloco com a informação do valor de LAMBDA por estágio
    no horizonte de execução.
    """

    BEGIN_PATTERN = "VALORES DE LAMBDA VARIAVEIS NO TEMPO"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_ano: List[Field] = [LiteralField(5, 0)]
        campos_valores: List[Field] = [
            FloatField(5, 7 * i + 7, 1) for i in range(len(MESES_DF))
        ]
        self.__linha = Line(campo_ano + campos_valores)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoLambdaVariavelNoTempo):
            return False
        bloco: BlocoLambdaVariavelNoTempo = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO):
        def converte_tabela_em_df():
            df = pd.DataFrame(tabela, columns=MESES_DF)
            df["Ano"] = anos
            df = df
            df = df[["Ano"] + MESES_DF]
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_ANOS_ESTUDO, len(MESES_DF)))
        anos: List[str] = []
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3:
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            anos.append(dados[0])
            tabela[i, :] = dados[1:]
            i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do cvar.dat não foram lidos com sucesso")

        for _, lin in self.data.iterrows():
            file.write(self.__linha.write(lin.tolist()))
