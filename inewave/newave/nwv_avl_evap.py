from inewave.newave.modelos.blocos.versaomodelo import VersaoModelo
from inewave.newave.modelos.nwv_avl_evap import TabelaAvlEvap

from inewave.newave.modelos.arquivoscsv.arquivocsv import ArquivoCSV
from typing import Optional
import pandas as pd  # type: ignore


class NwvAvlEvap(ArquivoCSV):
    """
    Arquivo com a avaliação da evaporação linear do NEWAVE.
    """

    BLOCKS = [VersaoModelo, TabelaAvlEvap]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, arquivo: str = "nwv_avl_evap.csv"
    ) -> "NwvAvlEvap":
        return cls.read(diretorio, arquivo)

    @property
    def tabela(self) -> Optional[pd.DataFrame]:
        """
        A tabela de dados que está contida no arquivo.

        - periodo (`int`)
        - indice_usina (`int`)
        - nome_usina (`str`)
        - volume_armazenado_hm3 (`float`)
        - evaporacao_calculada_hm3 (`float`)
        - evaporacao_modelo_hm3 (`float`)
        - desvio_absoluto_hm3 (`float`)
        - desvio_percentual (`float`)

        :return: A tabela como um dataframe
        :rtype: pd.DataFrame | None
        """
        return self._tabela()