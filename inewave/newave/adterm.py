from inewave.newave.modelos.adterm import BlocoUTEAdTerm

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Adterm(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às térmicas de
    despacho antecipado disponíveis.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoUTEAdTerm]

    @property
    def despachos(self) -> Optional[pd.DataFrame]:
        """
        A tabela de espachos antecipados das térmicas GNL.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - lag (`int`)
        - patamar (`int`)
        - valor (`float`)

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
