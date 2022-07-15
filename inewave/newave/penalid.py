from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional
import pandas as pd  # type: ignore

from inewave.newave.modelos.penalid import BlocoPenalidades


class Penalid(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às penalidades
    aplicadas por desvio.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [BlocoPenalidades]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="penalid.dat"
    ) -> "Penalid":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="penalid.dat"):
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
    def penalidades(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as penalidades.

        - Chave (`str`)
        - Penalidade 1 (`float`)
        - Penalidade 2 (`float`)
        - Subsistema (`int`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoPenalidades, 0)
        if b is not None:
            return b.data
        return None

    @penalidades.setter
    def penalidades(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoPenalidades, 0)
        if b is not None:
            b.data = df
