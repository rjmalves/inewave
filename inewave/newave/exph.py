from inewave.newave.modelos.exph import BlocoUHEExph

from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional
import pandas as pd  # type: ignore


class Exph(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à expansão
    hidraulica do sistema.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [BlocoUHEExph]

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="exph.dat") -> "Exph":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="exph.dat"):
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
    def expansoes(self) -> Optional[pd.DataFrame]:
        """
        A tabela de expansões de máquinas das UHEs.

        - Código UHE (`int`)
        - Nome UHE (`str`)
        - Início Enchimento (`datetime`)
        - Duração (`int`)
        - Volume Morto (`float`)
        - Data de Entrada (`datetime`)
        - Potência (`float`)
        - Máquina (`int`)
        - Conjunto (`int`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoUHEExph, 0)
        if b is not None:
            return b.data
        return None

    @expansoes.setter
    def expansoes(self, d: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoUHEExph, 0)
        if b is not None:
            b.data = d
