from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional

from inewave.newave.modelos.ghmin import BlocoUHEGhmin

import pandas as pd  # type: ignore


class Ghmin(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à geração hidráulica
    mínima por usina.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [BlocoUHEGhmin]

    @property
    def geracoes(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as gerações mínimas das usinas
        hidráulicas.

        - codigo_usina (`int`)
        - data (`datetime`)
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
