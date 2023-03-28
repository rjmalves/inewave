from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.energiab import SecaoDadosEnergiab
import pandas as pd  # type: ignore

from typing import TypeVar, Optional


class Energiab(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às séries sintéticas
    de energia para a etapa backward geradas pelo modelo.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosEnergiab]
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls,
        diretorio: str,
        nome_arquivo="energiab.dat",
        numero_forwards: int = 200,
        numero_aberturas: int = 20,
        numero_rees: int = 12,
        numero_estagios: int = 60,
    ) -> "Energiab":
        return cls.read(
            diretorio,
            nome_arquivo,
            numero_forwards=numero_forwards,
            numero_aberturas=numero_aberturas,
            numero_rees=numero_rees,
            numero_estagios=numero_estagios,
        )

    def escreve_arquivo(self, diretorio: str, nome_arquivo="energiab.dat"):
        self.write(diretorio, nome_arquivo)

    @property
    def series(self) -> Optional[pd.DataFrame]:
        """
        Obtém a tabela com os dados das séries de energia
        afluente por REE, por estágio, série forward e abertura.

        - estagio (`int`): estágio do cenário gerado
        - ree (`int`): REE para o qual foi gerado
        - serie (`int`): índice da série forward
        - abertura (`int`): índice da abertura
        - valor (`float`): energia em MWmes

        :return: A tabela com os dados das séries
        :rtype: pd.DataFrame | None
        """
        sections = [r for r in self.data.of_type(SecaoDadosEnergiab)]
        if len(sections) > 0:
            return sections[0].data
        else:
            return None

    @series.setter
    def series(self, df: pd.DataFrame):
        sections = [r for r in self.data.of_type(SecaoDadosEnergiab)]
        if len(sections) > 0:
            sections[0].data = df
