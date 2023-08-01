from inewave.newave.modelos.cvar import (
    BlocoValoresConstantesCVAR,
    BlocoAlfaVariavelNoTempo,
    BlocoLambdaVariavelNoTempo,
)

from cfinterface.files.blockfile import BlockFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


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

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="cvar.dat") -> "Cvar":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="cvar.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

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

        - ano (`str`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

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

        - ano (`str`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: O valor de LAMBDA por estágio em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoLambdaVariavelNoTempo)
        if isinstance(b, BlocoLambdaVariavelNoTempo):
            return b.data
        return None
