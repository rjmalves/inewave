from typing import Optional, TypeVar

import pandas as pd  # type: ignore
from cfinterface.files.sectionfile import SectionFile

from inewave.newave.modelos.vazpast import BlocoVazPast


class Vazpast(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às
    vazões anteriores ao período de planejamento.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que são usadas juntos das contidas no arquivo `vazoes.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoVazPast]

    @property
    def tendencia(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a tendência hidrológica por UHE.

        - codigo_posto (`int`)
        - nome_usina (`str`)
        - mes (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoVazPast)
        if isinstance(b, BlocoVazPast):
            return b.data
        return None

    @tendencia.setter
    def tendencia(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoVazPast)
        if isinstance(b, BlocoVazPast):
            b.data = df
