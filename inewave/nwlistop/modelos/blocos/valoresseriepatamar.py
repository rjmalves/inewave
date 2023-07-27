from cfinterface.components.block import Block
from cfinterface.components.line import Line

from inewave.config import MESES_DF, MAX_PATAMARES, MAX_SERIES_SINTETICAS
from inewave._utils.formatacao import formata_df_meses_para_datas_nwlistop

from typing import IO, List
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class ValoresSeriePatamar(Block):
    """
    Bloco com a informaçao de uma tabela por submercado, com
    entradas por série e patamar.
    """

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = " MEDIA"
    HEADER_LINE = Line([])
    DATA_LINE = Line([])

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_ano = self.__class__.HEADER_LINE
        self.__linha = self.__class__.DATA_LINE

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ValoresSeriePatamar):
            return False
        bloco: ValoresSeriePatamar = o
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
            cols = MESES_DF
            df = pd.DataFrame(tabela, columns=["serie"] + cols)
            df["ano"] = self.__ano
            df.loc[df["serie"].isna(), "serie"] = 1
            df["patamar"] = patamares
            df = df[["ano", "serie", "patamar"] + cols]
            df = df.astype({"serie": "int64", "ano": "int64"})
            return formata_df_meses_para_datas_nwlistop(df)

        self.__ano = self.__linha_ano.read(file.readline())[0]
        file.readline()

        # Variáveis auxiliares
        self.__serie_atual = 0
        tabela = np.zeros(
            (MAX_PATAMARES * MAX_SERIES_SINTETICAS, len(MESES_DF) + 1)
        )
        patamares: List[str] = []
        i = 0
        while True:
            linha = file.readline()
            if self.ends(linha) or len(linha) <= 1:
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
