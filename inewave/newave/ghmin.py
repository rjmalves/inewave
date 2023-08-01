from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional

from inewave.newave.modelos.ghmin import BlocoUHEGhmin

import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Ghmin(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à geração hidráulica
    mínima por usina.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [BlocoUHEGhmin]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="ghmin.dat") -> "Ghmin":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ghmin.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def geracoes(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as gerações mínimas das usinas
        hidráulicas.

        - codigo_usina (`int`)
        - mes (`int`)
        - ano (`str`)
        - patamar (`int`)
        - geracao (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoUHEGhmin)
        if isinstance(b, BlocoUHEGhmin):
            return b.data
        return None

    @geracoes.setter
    def geracoes(self, valor: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoUHEGhmin)
        if isinstance(b, BlocoUHEGhmin):
            b.data = valor
        else:
            raise ValueError("Campo não lido")
