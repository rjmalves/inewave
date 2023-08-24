from inewave.newave.modelos.clast import (
    BlocoUTEClasT,
    BlocoModificacaoUTEClasT,
)

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Clast(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às classes de
    usinas térmicas.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoUTEClasT, BlocoModificacaoUTEClasT]

    @property
    def usinas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as usinas e seus custos.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - tipo_combustivel (`str`)
        - indice_ano_estudo (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoUTEClasT)
        if isinstance(b, BlocoUTEClasT):
            return b.data
        return None

    @usinas.setter
    def usinas(self, valor: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoUTEClasT)
        if isinstance(b, BlocoUTEClasT):
            b.data = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def modificacoes(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as modificações de custos das usinas
        organizadas por usina.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - data_inicio (`datetime`)
        - data_fim (`datetime`)
        - custo (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoModificacaoUTEClasT)
        if isinstance(b, BlocoModificacaoUTEClasT):
            return b.data
        return None

    @modificacoes.setter
    def modificacoes(self, valor: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoModificacaoUTEClasT)
        if isinstance(b, BlocoModificacaoUTEClasT):
            b.data = valor
        else:
            raise ValueError("Campo não lido")
