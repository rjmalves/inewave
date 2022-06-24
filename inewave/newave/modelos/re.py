from inewave.config import MAX_RES

from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class BlocoUsinasConjuntoRE(Section):
    """
    Bloco com informações das usinas pertencentes a cada conjunto
    de restrições elétricas por conjunto de RE.
    """

    FIM_BLOCO = "999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        campo_conjunto: List[Field] = [IntegerField(3, 0)]
        campos_usinas: List[Field] = [
            IntegerField(3, 6 + i * 4) for i in range(10)
        ]
        self.__linha = Line(campo_conjunto + campos_usinas)
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoUsinasConjuntoRE):
            return False
        bloco: BlocoUsinasConjuntoRE = o
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
            cols = ["Conjunto"] + [f"Usina {i}" for i in range(1, 11)]
            df = pd.DataFrame(tabela, columns=cols)
            df = df.astype({"Conjunto": "int64"})
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_RES, 11))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoUsinasConjuntoRE.FIM_BLOCO in linha:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                tabela[i, :] = dados
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do re.dat não foram lidos com sucesso")

        for _, linha in self.data.iterrows():
            linha_escrita = []
            for v in linha:
                linha_escrita.append(None if np.isnan(v) else int(v))
            file.write(self.__linha.write(linha_escrita))
        file.write(BlocoUsinasConjuntoRE.FIM_BLOCO + "\n")


class BlocoConfiguracaoRestricoesRE(Section):
    """
    Bloco com informações de configuração das restrições elétricas
    para cada conjunto de usinas.
    """

    FIM_BLOCO = "999"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 0),
                IntegerField(2, 4),
                IntegerField(4, 7),
                IntegerField(2, 12),
                IntegerField(4, 15),
                IntegerField(1, 20),
                FloatField(15, 22, 2),
                LiteralField(23, 38),
            ]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoConfiguracaoRestricoesRE):
            return False
        bloco: BlocoConfiguracaoRestricoesRE = o
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
            cols = [
                "Conjunto",
                "Mês Início",
                "Ano Início",
                "Mês Fim",
                "Ano Fim",
                "Flag P",
                "Restrição",
            ]
            df = pd.DataFrame(tabela, columns=cols)
            df["Motivo"] = motivos
            df = df.astype(
                {
                    "Conjunto": "int64",
                    "Mês Início": "int64",
                    "Ano Início": "int64",
                    "Mês Fim": "int64",
                    "Ano Fim": "int64",
                    "Flag P": "int64",
                }
            )
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        motivos: List[str] = []
        tabela = np.zeros((MAX_RES, 7))
        while True:
            linha = file.readline()
            # Confere se terminaram
            if len(linha) < 3 or BlocoUsinasConjuntoRE.FIM_BLOCO in linha:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            # Confere se é uma linha de subsistema ou tabela
            else:
                dados = self.__linha.read(linha)
                tabela[i, :] = dados[:-1]
                motivos.append(dados[-1])
                i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do re.dat não foram lidos com sucesso")

        for _, dados_linhas in self.data.iterrows():
            file.write(self.__linha.write(dados_linhas))
        file.write(BlocoUsinasConjuntoRE.FIM_BLOCO + "\n")
