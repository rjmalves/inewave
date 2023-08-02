from inewave.newave.modelos.blocos.versaomodelo import VersaoModelo
from inewave.newave.modelos.nwv_cortes_evap import TabelaCortesEvap

from inewave.newave.modelos.arquivoscsv.arquivocsv import ArquivoCSV
from typing import Optional
import pandas as pd  # type: ignore


class NwvCortesEvap(ArquivoCSV):
    """
    Arquivo com os cortes da evaporação linear do NEWAVE.
    """

    BLOCKS = [VersaoModelo, TabelaCortesEvap]

    @property
    def tabela(self) -> Optional[pd.DataFrame]:
        """
        A tabela de dados que está contida no arquivo.

        - periodo (`int`)
        - indice_usina (`int`)
        - nome_usina (`str`)
        - derivada_cota_area (`float`)
        - derivada_volume_cota (`float`)
        - volume_referencia_hm3 (`float`)
        - evaporacao_referencia_hm3 (`float`)
        - coeficiente_volume (`float`)
        - rhs_volume (`float`)

        :return: A tabela como um dataframe
        :rtype: pd.DataFrame | None
        """
        return self._tabela()
