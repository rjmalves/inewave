from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.vazaoaf import SecaoDadosVazaoaf
import pandas as pd  # type: ignore

from typing import TypeVar, Optional


class Vazaoaf(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às séries sintéticas
    de vazão para a etapa forward geradas pelo modelo.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosVazaoaf]
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls,
        diretorio: str,
        nome_arquivo="vazaoaf.dat",
        numero_forwards: int = 200,
        numero_uhes: int = 164,
        numero_estagios: int = 60,
        numero_estagios_th: int = 12,
    ) -> "Vazaoaf":
        return cls.read(
            diretorio,
            nome_arquivo,
            numero_forwards=numero_forwards,
            numero_uhes=numero_uhes,
            numero_estagios=numero_estagios,
            numero_estagios_th=numero_estagios_th,
        )

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vazaoaf.dat"):
        self.write(diretorio, nome_arquivo)

    @property
    def series(self) -> Optional[pd.DataFrame]:
        """
        Obtém a tabela com os dados das séries de vazão
        afluente por UHE e por estágio.

        - estagio (`int`): estágio do cenário gerado
        - uhe (`int`): UHE para a qual foi gerado
        - serie (`int`): índice da série forward
        - valor (`float`): vazão em hm3

        :return: A tabela com os dados das séries
        :rtype: pd.DataFrame | None
        """
        sections = [r for r in self.data.of_type(SecaoDadosVazaoaf)]
        if len(sections) > 0:
            return sections[0].data
        else:
            return None

    @series.setter
    def series(self, df: pd.DataFrame):
        sections = [r for r in self.data.of_type(SecaoDadosVazaoaf)]
        if len(sections) > 0:
            sections[0].data = df
