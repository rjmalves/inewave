from cfinterface.files.sectionfile import SectionFile
from cfinterface.components.section import Section
from typing import TypeVar, List, Type, Optional

import pandas as pd  # type: ignore

from inewave.newave.modelos.ree import (
    BlocoReesSubmercados,
    BlocoFicticiasIndividualizado,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Ree(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às configurações
    dos REEs.

    """

    T = TypeVar("T")

    SECTIONS: List[Type[Section]] = [
        BlocoReesSubmercados,
        BlocoFicticiasIndividualizado,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="ree.dat") -> "Ree":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ree.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def rees(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os REES e os submercados

        - codigo (`int`)
        - nome (`str`)
        - submercado (`int`)
        - mes_fim_individualizado (`int`)
        - ano_fim_individualizado (`int`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoReesSubmercados)
        if isinstance(b, BlocoReesSubmercados):
            return b.data
        return None

    @rees.setter
    def rees(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoReesSubmercados)
        if isinstance(b, BlocoReesSubmercados):
            b.data = df

    @property
    def remocao_ficticias(self) -> Optional[int]:
        """
        Opção de remover usinas fictícias nos períodos individualizados.

        :return: O valor do campo.
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoFicticiasIndividualizado)
        if isinstance(b, BlocoFicticiasIndividualizado):
            return b.data[1]
        return None

    @remocao_ficticias.setter
    def remocao_ficticias(self, d: int):
        b = self.data.get_sections_of_type(BlocoFicticiasIndividualizado)
        if isinstance(b, BlocoFicticiasIndividualizado):
            b.data[1] = d
