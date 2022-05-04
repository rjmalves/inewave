from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar


class Penalid(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às penalidades
    aplicadas por desvio.

    """

    T = TypeVar("T")

    SECTIONS = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="penalid.dat"
    ) -> "Penalid":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="penalid.dat"):
        self.write(diretorio, nome_arquivo)
