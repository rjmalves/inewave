from inewave.newave.modelos.confhd import BlocoConfUHE

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Confhd(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às
    configurações das usinas hidrelétricas.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que podem ser modificadas através do arquivo `modif.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoConfUHE]

    @property
    def usinas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as usinas.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - posto (`int`)
        - codigo_usina_jusante (`int`)
        - ree (`int`)
        - volume_inicial_percentual (`float`)
        - usina_existente (`str`)
        - usina_modificada (`int`)
        - ano_inicio_historico (`int`)
        - ano_fim_historico (`int`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoConfUHE)
        if isinstance(b, BlocoConfUHE):
            return b.data
        return None

    @usinas.setter
    def usinas(self, valor: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoConfUHE)
        if isinstance(b, BlocoConfUHE):
            b.data = valor
        else:
            raise ValueError("Campo não lido")
