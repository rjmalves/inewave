from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class GHMin(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à geração hidráulica
    mínima por usina.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="ghmin.dat") -> "GHMin":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ghmin.dat"):
        self.write(diretorio, nome_arquivo)
