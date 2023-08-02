from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.engnat import SecaoDadosEngnat
import pandas as pd  # type: ignore

from typing import TypeVar, Optional


class Engnat(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às séries históricas
    de energia por configuração, calculadas a partir das séries históricas
    de vazão.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosEngnat]
    STORAGE = "BINARY"

    @property
    def series(self) -> Optional[pd.DataFrame]:
        """
        Obtém a tabela com os dados das séries de energia
        afluente por REE e por estágio.

        - configuracao (`int`): configuração da série histórica
        - data (`datetime`): data para o valor histórico
        - ree (`int`): REE para o qual foi gerado
        - valor (`float`): energia em MWmes

        :return: A tabela com os dados das séries
        :rtype: pd.DataFrame | None
        """
        sections = [r for r in self.data.of_type(SecaoDadosEngnat)]
        if len(sections) > 0:
            return sections[0].data
        else:
            return None

    @series.setter
    def series(self, df: pd.DataFrame):
        sections = [r for r in self.data.of_type(SecaoDadosEngnat)]
        if len(sections) > 0:
            sections[0].data = df
