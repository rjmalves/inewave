from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar


class Abertura(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao número de
    aberturas utilizadas por período.

    """

    T = TypeVar("T")

    SECTIONS = []

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="abertura.dat"
    ) -> "Abertura":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="abertura.dat"):
        self.write(diretorio, nome_arquivo)
