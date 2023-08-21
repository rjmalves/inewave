from inewave.newave.modelos.cadic import BlocoCargasAdicionais

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Cadic(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às cargas
    adicionais.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoCargasAdicionais]

    @property
    def cargas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as cargas adicionais por mês/ano e por subsistema
        para cada razão de carga adicional. As colunas são:

        - codigo_submercado (`int`)
        - nome_submercado (`str`)
        - razao (`str`)
        - data (`datetime`)
        - valor (`float`)

        **OBS:** Na existência de períodos PRE ou POS, são adotados os anos
        padrão "0001" para PRE e "9999" para POS.

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoCargasAdicionais)
        if isinstance(b, BlocoCargasAdicionais):
            return b.data
        return None

    @cargas.setter
    def cargas(self, valor: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoCargasAdicionais)
        if isinstance(b, BlocoCargasAdicionais):
            b.data = valor
        else:
            raise ValueError("Campo não lido")
