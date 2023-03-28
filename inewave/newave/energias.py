from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.energias import SecaoDadosEnergias
import pandas as pd  # type: ignore

from typing import TypeVar, Optional


class Energias(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às séries sintéticas
    de energia para a simulação final geradas pelo modelo.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosEnergias]
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls,
        diretorio: str,
        nome_arquivo="energias.dat",
        numero_series: int = 2000,
        numero_rees: int = 12,
        numero_estagios: int = 60,
        numero_estagios_th: int = 12,
    ) -> "Energias":
        return cls.read(
            diretorio,
            nome_arquivo,
            numero_series=numero_series,
            numero_rees=numero_rees,
            numero_estagios=numero_estagios,
            numero_estagios_th=numero_estagios_th,
        )

    def escreve_arquivo(self, diretorio: str, nome_arquivo="energias.dat"):
        self.write(diretorio, nome_arquivo)

    @property
    def series(self) -> Optional[pd.DataFrame]:
        """
        Obtém a tabela com os dados das séries de energia
        afluente por REE e por estágio, para a simulação final.

        - estagio (`int`): estágio do cenário gerado
        - ree (`int`): REE para o qual foi gerado
        - serie (`int`): índice da série sintética
        - valor (`float`): energia em MWmes

        :return: A tabela com os dados das séries
        :rtype: pd.DataFrame | None
        """
        sections = [r for r in self.data.of_type(SecaoDadosEnergias)]
        if len(sections) > 0:
            return sections[0].data
        else:
            return None

    @series.setter
    def series(self, df: pd.DataFrame):
        sections = [r for r in self.data.of_type(SecaoDadosEnergias)]
        if len(sections) > 0:
            sections[0].data = df
