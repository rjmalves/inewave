from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional
import pandas as pd  # type: ignore

from inewave.newave.modelos.penalid import BlocoPenalidades


from os.path import join


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

        - mnemonico (`str`)
        - penalidade_1 (`float`)
        - penalidade_2 (`float`)
        - submercado (`int`)

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
