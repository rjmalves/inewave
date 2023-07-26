from inewave.newave.modelos.blocos.versaomodelo import VersaoModelo
from inewave.newave.modelos.avl_cortesfpha_nwv import TabelaAvlCortesFpha

from inewave.newave.modelos.arquivoscsv.arquivocsv import ArquivoCSV
from typing import Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class AvlCortesFpha(ArquivoCSV):
    """
    Arquivo com os cortes da função de produção para as UHEs
    do NEWAVE.
    """

    BLOCKS = [VersaoModelo, TabelaAvlCortesFpha]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, arquivo: str = "avl_cortesfpha_nwv.csv"
    ) -> "AvlCortesFpha":
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
