from inewave.newave.modelos.blocos.versaomodelo import VersaoModelo
from inewave.newave.modelos.nwv_cortes_evap import TabelaCortesEvap

from inewave.newave.modelos.arquivoscsv.arquivocsv import ArquivoCSV
from typing import Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class NwvCortesEvap(ArquivoCSV):
    """
    Arquivo com os cortes da evaporação linear do NEWAVE.
    """

    BLOCKS = [VersaoModelo, TabelaCortesEvap]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, arquivo: str = "nwv_cortes_evap.csv"
    ) -> "NwvCortesEvap":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, arquivo))

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
