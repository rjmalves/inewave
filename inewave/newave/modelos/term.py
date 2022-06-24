from cfinterface.components.section import Section
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore

from inewave.config import MESES_DF, MAX_UTES


class BlocoTermUTE(Section):
    """
    Bloco de informações das classes de usinas térmicas
    existentes no arquivo do NEWAVE `term.dat`.
    """

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line(
            [
                IntegerField(3, 1),
                LiteralField(12, 5),
                FloatField(5, 19, 0),
                FloatField(4, 25, 0),
                FloatField(6, 31, 2),
                FloatField(6, 38, 2),
            ]
            + [FloatField(6, 45 + 7 * i, 2) for i in range(len(MESES_DF) + 1)]
        )
        self.__cabecalhos: List[str] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BlocoTermUTE):
            return False
        bloco: BlocoTermUTE = o
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
        def converte_tabela_em_df() -> pd.DataFrame:
            cols = (
                [
                    "Potência Instalada",
                    "FC Máximo",
                    "TEIF",
                    "Indisponibilidade Programada",
                ]
                + [f"GT Min {m}" for m in MESES_DF]
                + ["GT Min D+ Anos"]
            )
            df = pd.DataFrame(
                tabela,
                columns=cols,
            )
            df["Número"] = numeros
            df["Nome"] = nomes
            df = df[["Número", "Nome"] + cols]
            df = df.astype({"Número": "int64"})
            return df

        # Salta as linhas adicionais
        for _ in range(2):
            self.__cabecalhos.append(file.readline())

        i = 0
        tabela = np.zeros((MAX_UTES, len(MESES_DF) + 5))
        numeros: List[int] = []
        nomes: List[str] = []
        while True:
            linha = file.readline()
            # Confere se terminaram as usinas
            if len(linha) < 3:
                # Converte para df e salva na variável
                if i > 0:
                    tabela = tabela[:i, :]
                    self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            tabela[i, :] = dados[2:]
            numeros.append(dados[0])
            nomes.append(dados[1])
            i += 1

    # Override
    def write(self, file: IO):
        for linha in self.__cabecalhos:
            file.write(linha)
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Dados do term.dat não foram lidos com sucesso")

        for _, lin in self.data.iterrows():
            file.write(self.__linha.write(lin.tolist()))
