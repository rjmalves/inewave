from typing import Optional, TypeVar

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package
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
        Tabela com a tendência hidrológica por posto.

        - codigo_posto (`int`)
        - nome_posto (`str`)
        - mes (`int`)
        - valor (`float`)
        - codigo_usina (`int`)
        - nome_usina (`str`)

        As colunas ``codigo_usina`` e ``nome_usina`` estão descontinuadas:
        repetem ``codigo_posto`` e ``nome_posto``, que o arquivo sempre
        conteve, e serão removidas em uma versão futura. Na escrita, um
        DataFrame só com as colunas descontinuadas ainda é aceito, com um
        `DeprecationWarning`.

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoVazPast)
        if isinstance(b, BlocoVazPast):
            return b.data
        return None

    @tendencia.setter
    def tendencia(self, df: pd.DataFrame) -> None:
        b = self.data.get_sections_of_type(BlocoVazPast)
        if isinstance(b, BlocoVazPast):
            b.data = df
