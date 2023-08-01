from inewave.newave.modelos.newavetim import BlocoTemposEtapasTim

from cfinterface.files.blockfile import BlockFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Newavetim(BlockFile):
    """
    Armazena os dados de saída do NEWAVE referentes aos
    tempos de execução do programa.

    """

    T = TypeVar("T")

    BLOCKS = [BlocoTemposEtapasTim]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="newave.tim"
    ) -> "Newavetim":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

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
