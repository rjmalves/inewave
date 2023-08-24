from inewave.newave.modelos.agrint import (
    BlocoGruposAgrint,
    BlocoLimitesPorGrupoAgrint,
)

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Agrint(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos agrupamentos
    de intercâmbio.

    """

    T = TypeVar("T")

    SECTIONS = [
        BlocoGruposAgrint,
        BlocoLimitesPorGrupoAgrint,
    ]

    @property
    def agrupamentos(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os intercâmbios em cada agrupamento.

        - agrupamento (`int`)
        - submercado_de (`int`)
        - submercado_para (`int`)
        - coeficiente (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoGruposAgrint)
        if isinstance(b, BlocoGruposAgrint):
            return b.data
        return None

    @agrupamentos.setter
    def agrupamentos(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoGruposAgrint)
        if isinstance(b, BlocoGruposAgrint):
            b.data = df

    @property
    def limites_agrupamentos(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os limites dos agrupamentos de intercâmbio
        durante o período de estudo.

        - agrupamento (`int`)
        - data_inicio (`datetime`)
        - data_fim (`datetime`)
        - comentario (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoLimitesPorGrupoAgrint)
        if isinstance(b, BlocoLimitesPorGrupoAgrint):
            return b.data
        return None

    @limites_agrupamentos.setter
    def limites_agrupamentos(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoLimitesPorGrupoAgrint)
        if isinstance(b, BlocoLimitesPorGrupoAgrint):
            b.data = df
