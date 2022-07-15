from inewave.newave.modelos.re import (
    BlocoUsinasConjuntoRE,
    BlocoConfiguracaoRestricoesRE,
)

from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore


class RE(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às restrições
    elétricas existentes.

    """

    T = TypeVar("T")

    SECTIONS = [
        BlocoUsinasConjuntoRE,
        BlocoConfiguracaoRestricoesRE,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="re.dat") -> "RE":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="re.dat"):
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
    def usinas_conjuntos(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os conjuntos de usinas com restrições elétricas.

        - Conjunto (`int`)
        - Usina 1 (`float`)
        - Usina 2 (`float`)
        - ...
        - Usina N (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoUsinasConjuntoRE, 0)
        if b is not None:
            return b.data
        return None

    @usinas_conjuntos.setter
    def usinas_conjuntos(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoUsinasConjuntoRE, 0)
        if b is not None:
            b.data = df

    @property
    def restricoes(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as configurações das restrições elétricas.

        - Conjunto (`int`)
        - Mês Início (`int`)
        - Mês Fim (`int`)
        - Ano Início (`int`)
        - Ano Fim (`int`)
        - Flag P (`int`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoConfiguracaoRestricoesRE, 0)
        if b is not None:
            return b.data
        return None

    @restricoes.setter
    def restricoes(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoConfiguracaoRestricoesRE, 0)
        if b is not None:
            b.data = df
