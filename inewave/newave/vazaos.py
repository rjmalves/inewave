from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.vazaos import SecaoDadosVazaos
import pandas as pd  # type: ignore

from typing import TypeVar, Optional


class Vazaos(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às séries sintéticas
    de vazão para a simulação final geradas pelo modelo.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosVazaos]
    STORAGE = "BINARY"

    @property
    def series(self) -> Optional[pd.DataFrame]:
        """
        Obtém a tabela com os dados das séries de vazão
        afluente por UHE e por estágio.

        - estagio (`int`): estágio do cenário gerado
        - uhe (`int`): UHE para a qual foi gerado
        - serie (`int`): índice da série sintética
        - valor (`float`): vazão em hm3

        :return: A tabela com os dados das séries
        :rtype: pd.DataFrame | None
        """
        sections = [r for r in self.data.of_type(SecaoDadosVazaos)]
        if len(sections) > 0:
            return sections[0].data
        else:
            return None

    @series.setter
    def series(self, df: pd.DataFrame):
        sections = [r for r in self.data.of_type(SecaoDadosVazaos)]
        if len(sections) > 0:
            sections[0].data = df
