from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class Tecno(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às tecnologias
    disponíveis para geração de energia.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="tecno.dat") -> "Tecno":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="tecno.dat"):
        self.write(diretorio, nome_arquivo)
