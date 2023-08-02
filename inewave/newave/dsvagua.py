from inewave.newave.modelos.dsvagua import BlocoDsvUHE

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Dsvagua(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos
    desvios de água por usina.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que podem ser modificadas através do arquivo `dsvagua.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoDsvUHE]

    @property
    def desvios(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os desvios de água por usina e por estágio.

        - ano (`int`)
        - codigo_usina (`int`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)
        - considera_desvio_usina_NC (`int`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoDsvUHE)
        if isinstance(b, BlocoDsvUHE):
            return b.data
        return None

    @desvios.setter
    def desvios(self, valor: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoDsvUHE)
        if isinstance(b, BlocoDsvUHE):
            b.data = valor
        else:
            raise ValueError("Campo não lido")
