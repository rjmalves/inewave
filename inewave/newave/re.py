from inewave.newave.modelos.re import (
    BlocoUsinasConjuntoRE,
    BlocoConfiguracaoRestricoesRE,
)

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Re(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às restrições
    elétricas existentes.

    """

    T = TypeVar("T")

    SECTIONS = [
        BlocoUsinasConjuntoRE,
        BlocoConfiguracaoRestricoesRE,
    ]

    @property
    def usinas_conjuntos(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os conjuntos de usinas com restrições elétricas.

        - conjunto (`int`)
        - codigo_usina (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoUsinasConjuntoRE)
        if isinstance(b, BlocoUsinasConjuntoRE):
            return b.data
        return None

    @usinas_conjuntos.setter
    def usinas_conjuntos(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoUsinasConjuntoRE)
        if isinstance(b, BlocoUsinasConjuntoRE):
            b.data = df

    @property
    def restricoes(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as configurações das restrições elétricas.

        - conjunto (`int`)
        - mes_inicio (`int`)
        - mes_fim (`int`)
        - ano_inicio (`int`)
        - ano_fim (`int`)
        - patamar (`int`)
        - restricao (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoConfiguracaoRestricoesRE)
        if isinstance(b, BlocoConfiguracaoRestricoesRE):
            return b.data
        return None

    @restricoes.setter
    def restricoes(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoConfiguracaoRestricoesRE)
        if isinstance(b, BlocoConfiguracaoRestricoesRE):
            b.data = df
