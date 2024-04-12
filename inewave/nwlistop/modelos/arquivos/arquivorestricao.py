from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.blocos.valoresserie import (
    ValoresSerie,
)

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import TypeVar, Optional


class ArquivoRestricao(BlockFile):
    """
    Armazena os dados das saídas por usina.
    """

    __slots__ = ["__valores"]

    T = TypeVar("T")

    BLOCKS = [Restricao, ValoresSerie]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__valores = None

    def __monta_tabela(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(ValoresSerie):
            dados = b.data
            if dados is None:
                continue
            elif df is None:
                df = b.data
            else:
                df = pd.concat([df, b.data], ignore_index=True)
        return df

    @property
    def valores(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os valores, por série e
        por mês/ano de estudo.

        - data (`datetime`)
        - serie (`str`)
        - valor (`float`)

        :return: A tabela dos valores.
        :rtype: pd.DataFrame | None
        """
        if self.__valores is None:
            self.__valores = self.__monta_tabela()
        return self.__valores

    @property
    def restricao(self) -> Optional[int]:
        """
        A restrição associada ao arquivo lido.

        :return: O código da restrição
        :rtype: int
        """
        b = self.data.get_blocks_of_type(Restricao)
        if isinstance(b, Restricao):
            return b.data
        return None
