from cfinterface.components.block import Block
from cfinterface.components.line import Line

from inewave.config import (
    MESES_DF,
    MAX_PATAMARES,
    MAX_SERIES_SINTETICAS,
    MAX_UTES,
)
from inewave._utils.formatacao import formata_df_meses_para_datas_nwlistop

from typing import IO, List
import pandas as pd  # type: ignore
import numpy as np  # type: ignore


class ValoresClasseTermicaSeriePatamar(Block):
    """
    Bloco com a informaçao de uma tabela por submercado, com
    entradas por classe térmica, série e patamar.
    """

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = "  TOTAL "
    HEADER_LINE = Line([])
    DATA_LINE = Line([])

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_ano = self.__class__.HEADER_LINE
        self.__linha = self.__class__.DATA_LINE

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ValoresClasseTermicaSeriePatamar):
            return False
        bloco: ValoresClasseTermicaSeriePatamar = o
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
            df = pd.DataFrame(tabela, columns=["classe", "serie"] + cols)
            df["ano"] = self.__ano
            df["patamar"] = patamares
            df = df[["ano", "classe", "serie", "patamar"] + cols]
            df = df.astype(
                {"classe": "int64", "serie": "int64", "ano": "int64"}
            )
            return formata_df_meses_para_datas_nwlistop(df)

        self.__ano = self.__linha_ano.read(file.readline())[0]
        file.readline()

        # Variáveis auxiliares
        self.__classe_atual = 0
        self.__serie_atual = 0
        tabela = np.zeros(
            (
                MAX_PATAMARES * MAX_SERIES_SINTETICAS * MAX_UTES,
                len(MESES_DF) + 2,
            )
        )
        patamares: List[str] = []
        i = 0
        intervalo_classes = False
        while True:
            linha = file.readline()
            if self.ends(linha) or len(linha) <= 1:
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break

            if "  MEDIA        " in linha:
                intervalo_classes = True
                continue
            elif "  MAX          " in linha:
                intervalo_classes = False
                continue

            if intervalo_classes:
                continue
            dados = self.__linha.read(linha)
            if dados[0] is not None:
                self.__classe_atual = dados[0]
            if dados[1] is not None:
                self.__serie_atual = dados[1]
            tabela[i, 0] = self.__classe_atual
            tabela[i, 1] = self.__serie_atual
            patamares.append(dados[2])
            tabela[i, 2:] = dados[3:]
            i += 1
