from inewave.nwlistop.modelos.blocos.parsubmercados import ParSubmercados
from inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual import (
    TabelaSeriePatamarAnual,
)
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import Optional


class ArquivoParSubmercadoPatamar(BlockFile):
    """
    Armazena os dados das saídas por patamar, por par de submercados.
    """

    __slots__ = ["__valores"]

    BLOCKS = [ParSubmercados, ValoresSeriePatamar]

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
    def submercado_de(self) -> Optional[str]:
        """
        O submercado de origem associado ao arquivo lido.

        :return: Os nome do submercado
        :rtype: str
        """
        b = self.data.get_blocks_of_type(ParSubmercados)
        if isinstance(b, ParSubmercados):
            return b.data[0]
        return None

    @property
    def submercado_para(self) -> Optional[str]:
        """
        O submercado de destino associado ao arquivo lido.

        :return: Os nome do submercado
        :rtype: str
        """
        b = self.data.get_blocks_of_type(ParSubmercados)
        if isinstance(b, ParSubmercados):
            return b.data[1]
        return None
