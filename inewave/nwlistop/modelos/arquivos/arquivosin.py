from inewave.nwlistop.modelos.blocos.tabela_serie_anual import (
    TabelaSerieAnual,
)
from inewave.nwlistop.modelos.blocos.valoresserie import (
    ValoresSerie,
)

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import Optional


class ArquivoSIN(BlockFile):
    """
    Armazena os dados das saídas por submercado.
    """

    __slots__ = ["__valores"]

    BLOCKS = [ValoresSerie]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__valores = None

    def __monta_tabela(self) -> pd.DataFrame:
        dfs = [
            b.data
            for b in self.data
            if isinstance(b, (ValoresSerie, TabelaSerieAnual))
            and b.data is not None
        ]
        if not dfs:
            return None
        return pd.concat(dfs, ignore_index=True)

    @property
    def valores(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os valores por patamar, por série e
        por mês/ano de estudo.

        - data (`datetime`)
        - serie (`str`)
        - valor (`float`)

        :return: A tabela dos valores por patamar.
        :rtype: pd.DataFrame | None
        """
        if self.__valores is None:
            self.__valores = self.__monta_tabela()
        return self.__valores
