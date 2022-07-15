from inewave.newave.modelos.patamar import (
    BlocoNumeroPatamares,
    BlocoDuracaoPatamar,
    BlocoCargaPatamar,
    BlocoIntercambioPatamarSubsistemas,
    BlocoUsinasNaoSimuladas,
)

from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore


class Patamar(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos
    patamares de carga por submercado.

    """

    T = TypeVar("T")

    SECTIONS = [
        BlocoNumeroPatamares,
        BlocoDuracaoPatamar,
        BlocoCargaPatamar,
        BlocoIntercambioPatamarSubsistemas,
        BlocoUsinasNaoSimuladas,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="patamar.dat"
    ) -> "Patamar":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="patamar.dat"):
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
    def numero_patamares(self) -> Optional[int]:
        """
        O número de patamares utilizado no estudo.

        :return: O número de patamares como um inteiro
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoNumeroPatamares, 0)
        if b is not None:
            return b.data
        return None

    @numero_patamares.setter
    def numero_patamares(self, n: int):
        b = self.__bloco_por_tipo(BlocoNumeroPatamares, 0)
        if b is not None:
            b.data = n

    @property
    def duracao_mensal_patamares(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a duração mensal de cada patamar no horizonte
        de estudo.

        - Ano (`int`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A duração por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoDuracaoPatamar, 0)
        if b is not None:
            return b.data
        return None

    @duracao_mensal_patamares.setter
    def duracao_mensal_patamares(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoDuracaoPatamar, 0)
        if b is not None:
            b.data = df

    @property
    def carga_patamares(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a carga em P.U. por patamar.

        - Ano (`int`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A carga por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoCargaPatamar, 0)
        if b is not None:
            return b.data
        return None

    @carga_patamares.setter
    def carga_patamares(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoCargaPatamar, 0)
        if b is not None:
            b.data = df

    @property
    def intercambio_patamares(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a correção em P.U. do intercâmbio por patamar.

        - Subsistema De (`str`)
        - Subsistema Para (`str`)
        - Ano (`int`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A carga por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoIntercambioPatamarSubsistemas, 0)
        if b is not None:
            return b.data
        return None

    @intercambio_patamares.setter
    def intercambio_patamares(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoIntercambioPatamarSubsistemas, 0)
        if b is not None:
            b.data = df

    @property
    def usinas_nao_simuladas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os fatores das usinas não simuladas em P.U.

        - Subsistema (`str`)
        - Bloco (`int`)
        - Ano (`int`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: Os valores por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoUsinasNaoSimuladas, 0)
        if b is not None:
            return b.data
        return None

    @usinas_nao_simuladas.setter
    def usinas_nao_simuladas(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoUsinasNaoSimuladas, 0)
        if b is not None:
            b.data = df
