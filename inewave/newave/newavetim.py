from inewave.newave.modelos.newavetim import BlocoTemposEtapasTim

from cfinterface.files.blockfile import BlockFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Newavetim(BlockFile):
    """
    Armazena os dados de saída do NEWAVE referentes aos
    tempos de execução do programa.

    """

    T = TypeVar("T")

    BLOCKS = [BlocoTemposEtapasTim]

    @property
    def tempos_etapas(self) -> Optional[pd.DataFrame]:
        """
        Tempos de execução do modelo por etapa do modelo.

        - etapa (`str`)
        - tempo (`timedelta`)

        :return: Os tempos em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoTemposEtapasTim)
        if isinstance(b, BlocoTemposEtapasTim):
            return b.data
        return None
