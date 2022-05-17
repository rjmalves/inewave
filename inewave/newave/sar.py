from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class SAR(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à superfície de
    aversão à risco (SAR).

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="sar.dat") -> "SAR":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="sar.dat"):
        self.write(diretorio, nome_arquivo)
