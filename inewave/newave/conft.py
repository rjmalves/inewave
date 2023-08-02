from inewave.newave.modelos.conft import BlocoConfUTE

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Conft(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às configurações das
    usinas térmicas.
    """

    T = TypeVar("T")

    SECTIONS = [BlocoConfUTE]

    @property
    def usinas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as usinas.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - submercado (`int`)
        - usina_existente (`str`)
        - classe (`int`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoConfUTE)
        if isinstance(b, BlocoConfUTE):
            return b.data
        return None

    @usinas.setter
    def usinas(self, valor: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoConfUTE)
        if isinstance(b, BlocoConfUTE):
            b.data = valor
        else:
            raise ValueError("Campo não lido")
