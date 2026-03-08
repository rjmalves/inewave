import warnings
from typing import IO, Any, Optional

import numpy as np
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from cfinterface.components.block import Block
from cfinterface.components.line import Line

from inewave._utils.formatacao import formata_df_meses_para_datas_nwlistop
from inewave.config import MAX_SERIES_SINTETICAS, MESES_DF


class ValoresSerie(Block):
    """
    Bloco com a informaçao de uma tabela para o SIN, com
    entradas por série.

    .. deprecated::
        Use :class:`~inewave.nwlistop.modelos.blocos\
.tabela_serie_anual.TabelaSerieAnual` instead.
    """

    __slots__ = ["__linha", "__linha_ano", "__ano"]

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = "MEDIA "
    HEADER_LINE = Line([])
    DATA_LINE = Line([])

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        warnings.warn(
            "ValoresSerie is deprecated. Use TabelaSerieAnual instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(previous, next, data)
        self.__linha_ano = self.__class__.HEADER_LINE
        self.__linha = self.__class__.DATA_LINE

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ValoresSerie):
            return False
        if not isinstance(self.data, pd.DataFrame) or not isinstance(
            o.data, pd.DataFrame
        ):
            return False
        return bool(self.data.equals(o.data))

    # Override
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        def converte_tabela_em_df() -> pd.DataFrame:
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
