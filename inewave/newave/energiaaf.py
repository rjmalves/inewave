from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.energiaaf import SecaoDadosEnergiaaf
import pandas as pd  # type: ignore

from typing import TypeVar, Optional


class Energiaaf(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às séries sintéticas
    de energia para a etapa forward geradas pelo modelo.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosEnergiaaf]
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls,
        diretorio: str,
        nome_arquivo="energiaaf.dat",
        numero_forwards: int = 200,
        numero_rees: int = 12,
        numero_estagios: int = 60,
        numero_estagios_th: int = 12,
    ) -> "Energiaaf":
        return cls.read(
            diretorio,
            nome_arquivo,
            numero_forwards=numero_forwards,
            numero_rees=numero_rees,
            numero_estagios=numero_estagios,
            numero_estagios_th=numero_estagios_th,
        )

    def escreve_arquivo(self, diretorio: str, nome_arquivo="energiaaf.dat"):
        self.write(diretorio, nome_arquivo)

    @property
    def series(self) -> Optional[pd.DataFrame]:
        """
        Obtém a tabela com os dados das séries de energia
        afluente por REE e por estágio.

        - estagio (`int`): estágio do cenário gerado
        - ree (`int`): REE para o qual foi gerado
        - serie (`int`): índice da série forward
        - valor (`float`): energia em MWmes

        :return: A tabela com os dados das séries
        :rtype: pd.DataFrame | None
        """
        sections = [r for r in self.data.of_type(SecaoDadosEnergiaaf)]
        if len(sections) > 0:
            return sections[0].data
        else:
            return None

    @series.setter
    def series(self, df: pd.DataFrame):
        sections = [r for r in self.data.of_type(SecaoDadosEnergiaaf)]
        if len(sections) > 0:
            sections[0].data = df
