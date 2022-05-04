from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar


class Expt(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à expansão
    térmica do sistema.

    """

    T = TypeVar("T")

    SECTIONS = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="expt.dat") -> "Expt":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="expt.dat"):
        self.write(diretorio, nome_arquivo)
