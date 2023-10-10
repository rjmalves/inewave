from inewave.newave.modelos.volref_saz import BlocoVolrefSaz

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class VolrefSaz(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos
    volumes de referência sazonais para as usinas.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que são usadas para fins de cálculos da evaporação linear e ajustes
    da FPHA.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoVolrefSaz]

    @property
    def volumes(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os volumes de referência sazonais por UHE.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - mes (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoVolrefSaz)
        if isinstance(b, BlocoVolrefSaz):
            return b.data
        return None

    @volumes.setter
    def volumes(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoVolrefSaz)
        if isinstance(b, BlocoVolrefSaz):
            b.data = df
