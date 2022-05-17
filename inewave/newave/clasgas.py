from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type


class ClasGas(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às classes
    de gás.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="clasgas.dat"
    ) -> "ClasGas":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="clasgas.dat"):
        self.write(diretorio, nome_arquivo)
