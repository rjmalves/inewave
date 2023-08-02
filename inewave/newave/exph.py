from inewave.newave.modelos.exph import BlocoUHEExph

from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional
import pandas as pd  # type: ignore


class Exph(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes à expansão
    hidraulica do sistema.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [BlocoUHEExph]

    @property
    def expansoes(self) -> Optional[pd.DataFrame]:
        """
        A tabela de expansões de máquinas das UHEs.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - data_inicio_enchimento (`datetime`)
        - duracao_enchimento (`int`)
        - volume_morto (`float`)
        - data_entrada_operacao (`datetime`)
        - potencia_instalada (`float`)
        - maquina_entrada (`int`)
        - conjunto_maquina_entrada (`int`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoUHEExph)
        if isinstance(b, BlocoUHEExph):
            return b.data
        return None

    @expansoes.setter
    def expansoes(self, d: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoUHEExph)
        if isinstance(b, BlocoUHEExph):
            b.data = d
