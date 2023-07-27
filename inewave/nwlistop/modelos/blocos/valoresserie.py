from cfinterface.components.block import Block
from cfinterface.components.line import Line

from inewave.config import MESES_DF, MAX_SERIES_SINTETICAS
from inewave._utils.formatacao import formata_df_meses_para_datas_nwlistop

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
    def read(self, file: IO, *args, **kwargs):
        def converte_tabela_em_df():
            cols = ["serie"] + MESES_DF
            df = pd.DataFrame(tabela, columns=cols)
            df["ano"] = self.__ano
            df.loc[df["serie"].isna(), "serie"] = 1
            df = df[["ano"] + cols]
            df = df.astype({"serie": "int64", "ano": "int64"})
            return formata_df_meses_para_datas_nwlistop(df)

        self.__ano = self.__linha_ano.read(file.readline())[0]
        file.readline()

        # Variáveis auxiliares
        tabela = np.zeros((MAX_SERIES_SINTETICAS, len(MESES_DF) + 1))
        i = 0
        while True:
            linha = file.readline()
            if self.ends(linha) or len(linha) <= 1:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            tabela[i, :] = self.__linha.read(linha)
            i += 1
