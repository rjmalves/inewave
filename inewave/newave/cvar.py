from inewave.newave.modelos.cvar import (
    BlocoValoresConstantesCVAR,
    BlocoAlfaVariavelNoTempo,
    BlocoLambdaVariavelNoTempo,
)

from cfinterface.files.blockfile import BlockFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore


class CVAR(BlockFile):
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
    def le_arquivo(cls, diretorio: str, nome_arquivo="cvar.dat") -> "CVAR":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="cvar.dat"):
        self.write(diretorio, nome_arquivo)

    def __bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int
        :return: O gerador de blocos, se houver
        :rtype: Optional[Generator[T], None, None]
        """
        try:
            return next(
                b
                for i, b in enumerate(self.data.of_type(bloco))
                if i == indice
            )
        except StopIteration:
            return None

    @property
    def valores_constantes(self) -> Optional[list]:
        """
        Valores constantes dos parâmetros ALFA e LAMBDA do CVAR.

        :return: Os valores dos campos da linha como uma lista.
        :rtype: list | None
        """
        b = self.__bloco_por_tipo(BlocoValoresConstantesCVAR, 0)
        if b is not None:
            return b.data
        return None

    @valores_constantes.setter
    def valores_constantes(self, valores: list):
        """
        Valores constantes dos parâmetros ALFA e LAMBDA do CVAR.

        :return: Os valores dos campos da linha como uma lista.
        :rtype: list | None
        """
        b = self.__bloco_por_tipo(BlocoValoresConstantesCVAR, 0)
        if b is not None:
            b.data = valores
        else:
            raise ValueError("Bloco não lido")

    @property
    def alfa_variavel(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os valores variáveis do CVAR para o parâmetro ALFA.

        - Ano (`str`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: O valor de ALFA por estágio em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoAlfaVariavelNoTempo, 0)
        if b is not None:
            return b.data
        return None

    @property
    def lambda_variavel(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os valores variáveis do CVAR para o parâmetro LAMBDA.

        - Ano (`str`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: O valor de LAMBDA por estágio em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoLambdaVariavelNoTempo, 0)
        if b is not None:
            return b.data
        return None
