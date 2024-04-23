from inewave.newave.modelos.blocos.versaomodelo import VersaoModelo
from inewave.newave.modelos.nwv_eco_evap import TabelaEcoEvap

from inewave.newave.modelos.arquivoscsv.arquivocsv import ArquivoCSV
from typing import Optional
import pandas as pd  # type: ignore

from warnings import warn


class NwvEcoEvap(ArquivoCSV):
    """
    Arquivo com o eco dos dados da evaporação linear do NEWAVE.
    """

    BLOCKS = [VersaoModelo, TabelaEcoEvap]

    @property
    def tabela(self) -> Optional[pd.DataFrame]:
        """
        A tabela de dados que está contida no arquivo.

        - periodo (`int`)
        - codigo_usina (`int`)
        - nome_usina (`str`)
        - volume_referencia_hm3 (`float`)
        - evaporacao_referencia_hm3 (`float`)
        - coeficiente_evaporacao_mm_mes (`int`)
        - flag_evaporacao (`int`)
        - evaporacao_linear (`int`)
        - tipo_volume_referencia (`int`)

        :return: A tabela como um dataframe
        :rtype: pd.DataFrame | None
        """
        return self._tabela()

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe EvapEco no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
