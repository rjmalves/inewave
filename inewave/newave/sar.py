from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar


class SAR(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à superfície de
    aversão à risco (SAR).

    """

    T = TypeVar("T")

    SECTIONS = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="sar.dat") -> "SAR":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="sar.dat"):
        self.write(diretorio, nome_arquivo)
