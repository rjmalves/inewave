from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.vazinat import SecaoDadosVazinat
import pandas as pd  # type: ignore

from typing import TypeVar, Optional


class Vazinat(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às séries históricas
    de vazão por UHE.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosVazinat]
    STORAGE = "BINARY"

    @property
    def series(self) -> Optional[pd.DataFrame]:
        """
        Obtém a tabela com os dados das séries de vazão
        incremental por UHE.

        - data (`datetime`): data para o valor histórico
        - indice_usina (`int`): índice da usina conforme ordem de
            declaração no arquivo de configuração de usinas hidrelétricas
        - valor (`float`): vazão incremental em m3/s

        :return: A tabela com os dados das séries
        :rtype: pd.DataFrame | None
        """
        sections = [r for r in self.data.of_type(SecaoDadosVazinat)]
        if len(sections) > 0:
            return sections[0].data
        else:
            return None

    @series.setter
    def series(self, df: pd.DataFrame):
        sections = [r for r in self.data.of_type(SecaoDadosVazinat)]
        if len(sections) > 0:
            sections[0].data = df
