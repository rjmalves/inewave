from inewave.newave.modelos.shist import (
    BlocoVarreduraShist,
    BlocoSeriesSimulacaoShist,
)

from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional


class Shist(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à varredura
    das séries históricas para simulação.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [
        BlocoVarreduraShist,
        BlocoSeriesSimulacaoShist,
    ]

    @property
    def varredura(self) -> Optional[int]:
        """
        Flag para habilitar o uso de varredura na simulação.

        :return: O valor do flag
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoVarreduraShist)
        if isinstance(b, BlocoVarreduraShist):
            return b.data[0]
        return None

    @varredura.setter
    def varredura(self, valor: int):
        b = self.data.get_sections_of_type(BlocoVarreduraShist)
        if isinstance(b, BlocoVarreduraShist):
            b.data[0] = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def ano_inicio_varredura(self) -> Optional[int]:
        """
        O ano de início da varredura na simulação.

        :return: O ano
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoVarreduraShist)
        if isinstance(b, BlocoVarreduraShist):
            return b.data[1]
        return None

    @ano_inicio_varredura.setter
    def ano_inicio_varredura(self, valor: int):
        b = self.data.get_sections_of_type(BlocoVarreduraShist)
        if isinstance(b, BlocoVarreduraShist):
            b.data[1] = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def anos_inicio_simulacoes(self) -> Optional[List[int]]:
        """
        Os anos de início das simulações.

        :return: Os anos
        :rtype: list[int] | None
        """
        b = self.data.get_sections_of_type(BlocoSeriesSimulacaoShist)
        if isinstance(b, BlocoSeriesSimulacaoShist):
            return b.data
        return None

    @anos_inicio_simulacoes.setter
    def anos_inicio_simulacoes(self, valor: List[int]):
        b = self.data.get_sections_of_type(BlocoSeriesSimulacaoShist)
        if isinstance(b, BlocoSeriesSimulacaoShist):
            b.data = valor
        else:
            raise ValueError("Campo não lido")
