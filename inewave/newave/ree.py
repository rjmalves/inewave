from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional

import pandas as pd  # type: ignore

from inewave.newave.modelos.ree import (
    BlocoReesSubmercados,
    BlocoFicticiasIndividualizado,
)


class REE(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às configurações
    dos REEs.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [
        BlocoReesSubmercados,
        BlocoFicticiasIndividualizado,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="ree.dat") -> "REE":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ree.dat"):
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
    def rees(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os REES e os submercados

        - Número (`int`)
        - Nome (`str`)
        - Submercado (`int`)
        - Mês Fim Individualizado (`int`)
        - Ano Fim Individualizado (`int`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoReesSubmercados, 0)
        if b is not None:
            return b.data
        return None

    @rees.setter
    def rees(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoReesSubmercados, 0)
        if b is not None:
            b.data = df

    @property
    def remocao_ficticias(self) -> Optional[int]:
        """
        Opção de remover usinas fictícias nos períodos individualizados.

        :return: O valor do campo.
        :rtype: int | None
        """
        b = self.__bloco_por_tipo(BlocoFicticiasIndividualizado, 0)
        if b is not None:
            return b.data[1]
        return None

    @remocao_ficticias.setter
    def remocao_ficticias(self, d: int):
        b = self.__bloco_por_tipo(BlocoFicticiasIndividualizado, 0)
        if b is not None:
            b.data[1] = d
