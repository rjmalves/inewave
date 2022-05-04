from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar


class ElNino(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao fenômeno
    El Niño.

    """

    T = TypeVar("T")

    SECTIONS = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="elnino.dat") -> "ElNino":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="elnino.dat"):
        self.write(diretorio, nome_arquivo)
