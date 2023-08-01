from inewave.newave.modelos.adterm import BlocoUTEAdTerm

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Adterm(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às térmicas de
    despacho antecipado disponíveis.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoUTEAdTerm]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="adterm.dat") -> "Adterm":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="adterm.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def despachos(self) -> Optional[pd.DataFrame]:
        """
        A tabela de espachos antecipados das térmicas GNL.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - lag (`int`)
        - patamar_1 (`float`)
        - ...
        - patamar_N (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoUTEAdTerm)
        if isinstance(b, BlocoUTEAdTerm):
            return b.data
        return None

    @despachos.setter
    def despachos(self, d: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoUTEAdTerm)
        if isinstance(b, BlocoUTEAdTerm):
            b.data = d
