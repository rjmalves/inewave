from cfinterface.components.block import Block
from cfinterface.components.line import Line

from inewave.config import MESES_DF, MAX_SERIES_SINTETICAS

from typing import IO
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class ValoresSerie(Block):
    """
    Bloco com a informaçao de uma tabela para o SIN, com
    entradas por série.
    """

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = "MEDIA  "
    HEADER_LINE = Line([])
    DATA_LINE = Line([])

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_ano = self.__class__.HEADER_LINE
        self.__linha = self.__class__.DATA_LINE

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ValoresSerie):
            return False
        bloco: ValoresSerie = o
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
            df["Ano"] = self.__ano
            df = df[["Ano"] + cols]
            df = df.astype({"Série": "int64", "Ano": "int64"})
            return df

        self.__ano = self.__linha_ano.read(file.readline())[0]
        file.readline()

        # Variáveis auxiliares
        tabela = np.zeros((MAX_SERIES_SINTETICAS, len(MESES_DF) + 2))
        i = 0
        while True:
            linha = file.readline()
            if self.ends(linha):
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            tabela[i, :] = self.__linha.read(linha)
            i += 1
