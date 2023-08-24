from inewave.newave.modelos.term import BlocoTermUTE

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Term(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos dados das
    usinas térmicas.
    """

    T = TypeVar("T")

    SECTIONS = [BlocoTermUTE]

    @property
    def usinas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com configurações e inflexibilidades das usinas térmicas.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - potencia_instalada (`float`)
        - fator_capacidade_maximo (`float`)
        - teif (`float`)
        - indisponibilidade_programada (`float`)
        - mes (`int`)
        - geracao_minima (`float`)

        **OBS:** O mês de validade para a geração mínima
        pertence ao intervalo [1, 13], onde 13 vale para
        o 13º mês em diante.

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoTermUTE)
        if isinstance(b, BlocoTermUTE):
            return b.data
        return None

    @usinas.setter
    def usinas(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoTermUTE)
        if isinstance(b, BlocoTermUTE):
            b.data = df
