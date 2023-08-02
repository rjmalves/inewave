from inewave.newave.modelos.blocos.versaomodelo import VersaoModelo
from inewave.newave.modelos.avl_cortesfpha_nwv import TabelaAvlCortesFpha

from inewave.newave.modelos.arquivoscsv.arquivocsv import ArquivoCSV
from typing import Optional
import pandas as pd  # type: ignore


class AvlCortesFpha(ArquivoCSV):
    """
    Arquivo com os cortes da função de produção para as UHEs
    do NEWAVE.
    """

    BLOCKS = [VersaoModelo, TabelaAvlCortesFpha]

    @property
    def tabela(self) -> Optional[pd.DataFrame]:
        """
        A tabela de dados que está contida no arquivo.

        - codigo_usina (`int`)
        - periodo (`int`)
        - nome_usina (`str`)
        - indice_corte (`int`)
        - fator_correcao (`float`)
        - rhs_energia (`float`)
        - coeficiente_volume_util_MW_hm3 (`float`)
        - coeficiente_vazao_turbinada_MW_m3s (`float`)
        - coeficiente_vazao_vertida_MW_m3s (`float`)
        - coeficiente_vazao_lateral_MW_m3s (`float`)

        :return: A tabela como um dataframe
        :rtype: pd.DataFrame | None
        """
        return self._tabela()
