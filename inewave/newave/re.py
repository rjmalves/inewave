from inewave.newave.modelos.re import (
    BlocoUsinasConjuntoRE,
    BlocoConfiguracaoRestricoesRE,
)

from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


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
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="re.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

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

        - conjunto (`int`)
        - codigo_usina_1 (`float`)
        - codigo_usina_2 (`float`)
        - ...
        - codigo_usina_N (`float`)

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

        - conjunto (`int`)
        - mes_inicio (`int`)
        - mes_fim (`int`)
        - ano_inicio (`int`)
        - ano_fim (`int`)
        - patamar (`int`)
        - restricao (`float`)

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
