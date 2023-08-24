from inewave.newave.modelos.cvar import (
    BlocoValoresConstantesCVAR,
    BlocoAlfaVariavelNoTempo,
    BlocoLambdaVariavelNoTempo,
)

from cfinterface.files.blockfile import BlockFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Cvar(BlockFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à curva para
    penalização por volume mínimo dos reservatórios.
    """

    T = TypeVar("T")

    BLOCKS = [
        BlocoValoresConstantesCVAR,
        BlocoAlfaVariavelNoTempo,
        BlocoLambdaVariavelNoTempo,
    ]

    @property
    def valores_constantes(self) -> Optional[list]:
        """
        Valores constantes dos parâmetros ALFA e LAMBDA do CVAR.

        :return: Os valores dos campos da linha como uma lista.
        :rtype: list | None
        """
        b = self.data.get_blocks_of_type(BlocoValoresConstantesCVAR)
        if isinstance(b, BlocoValoresConstantesCVAR):
            return b.data
        return None

    @valores_constantes.setter
    def valores_constantes(self, valores: list):
        """
        Valores constantes dos parâmetros ALFA e LAMBDA do CVAR.

        :return: Os valores dos campos da linha como uma lista.
        :rtype: list | None
        """
        b = self.data.get_blocks_of_type(BlocoValoresConstantesCVAR)
        if isinstance(b, BlocoValoresConstantesCVAR):
            b.data = valores
        else:
            raise ValueError("Bloco não lido")

    @property
    def alfa_variavel(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os valores variáveis do CVAR para o parâmetro ALFA.

        - data (`datetime`)
        - valor (`float`)

        **OBS:** Na existência de períodos PRE ou POS, são adotados os anos
        padrão "0001" para PRE e "9999" para POS.


        :return: O valor de ALFA por estágio em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoAlfaVariavelNoTempo)
        if isinstance(b, BlocoAlfaVariavelNoTempo):
            return b.data
        return None

    @property
    def lambda_variavel(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os valores variáveis do CVAR para o parâmetro LAMBDA.

        - data (`datetime`)
        - valor (`float`)

        **OBS:** Na existência de períodos PRE ou POS, são adotados os anos
        padrão "0001" para PRE e "9999" para POS.


        :return: O valor de LAMBDA por estágio em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoLambdaVariavelNoTempo)
        if isinstance(b, BlocoLambdaVariavelNoTempo):
            return b.data
        return None
