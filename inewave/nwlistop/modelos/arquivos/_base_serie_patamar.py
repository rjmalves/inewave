from typing import Any, Iterable, Optional, cast

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
from cfinterface.components.block import Block
from cfinterface.files.blockfile import BlockFile

from inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual import (
    TabelaSeriePatamarAnual,
)
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class _ArquivoSeriePatamarBase(BlockFile):
    """
    Classe base para arquivos de saída do NWLISTOP com patamar.

    Subclasses devem declarar BLOCKS como atributo de classe.
    """

    __slots__ = ["__valores"]

    _DATA_BLOCK_TYPES: tuple[type, ...] = (
        ValoresSeriePatamar,
        TabelaSeriePatamarAnual,
    )

    def __init__(self, data: Any = ...) -> None:
        super().__init__(data)
        self.__valores: Optional[pd.DataFrame] = None

    def _monta_tabela(self) -> Optional[pd.DataFrame]:
        dfs = [
            b.data
            for b in cast(Iterable[Block], self.data)
            if isinstance(b, self._DATA_BLOCK_TYPES) and b.data is not None
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
            self.__valores = self._monta_tabela()
        return self.__valores
