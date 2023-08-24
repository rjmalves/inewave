from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional
import pandas as pd  # type: ignore

from inewave.newave.modelos.penalid import BlocoPenalidades


class Penalid(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às penalidades
    aplicadas por desvio.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [BlocoPenalidades]

    @property
    def penalidades(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as penalidades.

        - variavel (`str`)
        - codigo_ree_submercado (`int`)
        - patamar_penalidade (`int`)
        - patamar_carga (`int`)
        - valor_R$_MWh (`float`)
        - valor_R$_hm3 (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoPenalidades)
        if isinstance(b, BlocoPenalidades):
            return b.data
        return None

    @penalidades.setter
    def penalidades(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoPenalidades)
        if isinstance(b, BlocoPenalidades):
            b.data = df
