from inewave.newave.modelos.expt import BlocoUTEExpt

from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional
import pandas as pd  # type: ignore


class Expt(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à expansão
    térmica do sistema.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [BlocoUTEExpt]

    @property
    def expansoes(self) -> Optional[pd.DataFrame]:
        """
        A tabela de expansões das UTEs.

        - codigo_usina (`int`)
        - tipo (`str`)
        - modificacao (`float`)
        - data_inicio (`datetime`)
        - data_fim (`datetime`)
        - nome_usina (`str`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoUTEExpt)
        if isinstance(b, BlocoUTEExpt):
            return b.data
        return None

    @expansoes.setter
    def expansoes(self, d: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoUTEExpt)
        if isinstance(b, BlocoUTEExpt):
            b.data = d
