from inewave.newave.modelos.eafpast import BlocoEafPast

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Eafpast(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às
    vazões anteriores ao período de planejamento por REE.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que são usadas junto das contidas no arquivo `vazoes.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoEafPast]

    @property
    def tendencia(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a tendência hidrológica por REE.

        - codigo_ree (`int`)
        - nome_ree (`str`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: A tabela como um DataFrame
        :rtype: Optional[pd.DataFrame]
        """
        b = self.data.get_sections_of_type(BlocoEafPast)
        if isinstance(b, BlocoEafPast):
            return b.data
        return None

    @tendencia.setter
    def tendencia(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoEafPast)
        if isinstance(b, BlocoEafPast):
            b.data = df
