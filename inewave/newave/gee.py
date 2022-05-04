from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar


class GEE(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às configurações
    de emissão de Gases de Efeito Estufa (GEE).

    """

    T = TypeVar("T")

    SECTIONS = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="gee.dat") -> "GEE":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="gee.dat"):
        self.write(diretorio, nome_arquivo)
