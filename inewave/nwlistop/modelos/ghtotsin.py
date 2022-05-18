from inewave.config import MESES_DF, MAX_PATAMARES, MAX_SERIES_SINTETICAS

from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class GHAnos(Block):
    """
    Bloco com as informações das tabelas de geração hidráulica.
    """

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = " MEDIA"

    def __init__(self, state=..., previous=None, next=None, data=None) -> None:
        super().__init__(state, previous, next, data)
        self.__linha_ano = Line([IntegerField(4, 10)])
        campos_serie_patamar: List[Field] = [
            IntegerField(4, 2),
            LiteralField(5, 6),
        ]
        campos_custos: List[Field] = [
            FloatField(8, 12 + 9 * i, 1) for i in range(len(MESES_DF) + 1)
        ]
        self.__linha = Line(campos_serie_patamar + campos_custos)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, GHAnos):
            return False
        bloco: GHAnos = o
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
            cols = ["Série"] + MESES_DF + ["Média"]
            df = pd.DataFrame(tabela, columns=cols)
            df["Patamar"] = patamares
            df["Ano"] = self.__ano
            df = df[["Ano", "Série", "Patamar"] + MESES_DF + ["Média"]]
            df = df.astype({"Série": "int64", "Ano": "int64"})
            return df

        self.__ano = self.__linha_ano.read(file.readline())[0]
        file.readline()

        # Variáveis auxiliares
        self.__serie_atual = 0
        tabela = np.zeros(
            (MAX_PATAMARES * MAX_SERIES_SINTETICAS, len(MESES_DF) + 2)
        )
        i = 0
        patamares: List[str] = []
        while True:
            linha = file.readline()
            if self.ends(linha):
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            if dados[0] is not None:
                self.__serie_atual = dados[0]
            tabela[i, 0] = self.__serie_atual
            patamares.append(dados[1])
            tabela[i, 1:] = dados[2:]
            i += 1
