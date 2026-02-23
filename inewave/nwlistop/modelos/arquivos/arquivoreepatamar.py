from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual import (
    TabelaSeriePatamarAnual,
)
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import Optional


class ArquivoREEPatamar(BlockFile):
    """
    Armazena os dados das saídas por patamar, por REE.
    """

    __slots__ = ["__valores"]

    BLOCKS = [REE, ValoresSeriePatamar]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__valores = None

    def __monta_tabela(self) -> pd.DataFrame:
        dfs = [
            b.data
            for b in self.data
            if isinstance(b, (ValoresSeriePatamar, TabelaSeriePatamarAnual))
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
        - patamar (`str`)
        - serie (`str`)
        - valor (`float`)

        :return: A tabela dos valores por patamar.
        :rtype: pd.DataFrame | None
        """
        if self.__valores is None:
            self.__valores = self.__monta_tabela()
        return self.__valores

    @property
    def ree(self) -> Optional[str]:
        """
        O REE associado ao arquivo lido.

        :return: O nome do REE
        :rtype: str
        """
        b = self.data.get_blocks_of_type(REE)
        if isinstance(b, REE):
            return b.data
        return None
