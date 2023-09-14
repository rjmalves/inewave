from inewave.newave.modelos.blocos.versaomodelo import VersaoModelo
from inewave.newave.modelos.eco_fpha import TabelaEcoFpha

from inewave.newave.modelos.arquivoscsv.arquivocsv import ArquivoCSV
from typing import Optional
import pandas as pd  # type: ignore


class EcoFpha(ArquivoCSV):
    """
    Arquivo com o eco da função de produção para as UHEs
    do NEWAVE.
    """

    BLOCKS = [VersaoModelo, TabelaEcoFpha]

    @property
    def tabela(self) -> Optional[pd.DataFrame]:
        """
        A tabela de dados que está contida no arquivo.

        - codigo_usina (`int`)
        - periodo (`int`)
        - nome_usina (`str`)
        - tipo (`int`)
        - conv (`int`)
        - alfa (`int`)
        - rems (`int`)
        - numero_pontos_vazao_turbinada (`int`)
        - vazao_turbinada_minima (`float`)
        - vazao_turbinada_maxima (`float`)
        - numero_pontos_volume_armazenado (`int`)
        - volume_armazenado_minimo (`float`)
        - volume_armazenado_maximo (`float`)
        - geracao_minima (`float`)
        - geracao_maxima (`float`)

        :return: A tabela como um dataframe
        :rtype: pd.DataFrame | None
        """
        return self._tabela()
