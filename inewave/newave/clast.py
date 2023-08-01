from inewave.newave.modelos.clast import (
    BlocoUTEClasT,
    BlocoModificacaoUTEClasT,
)

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Clast(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às classes de
    usinas térmicas.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoUTEClasT, BlocoModificacaoUTEClasT]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="clast.dat") -> "Clast":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="clast.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def usinas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as usinas e seus custos.

        - codigo (`int`)
        - nome (`str`)
        - tipo_combustivel (`str`)
        - custo_1 (`float`)
        - ...
        - custo_5 (`float`)

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

        - codigo (`int`)
        - custo (`float`)
        - mes_inicio (`int`)
        - ano_inicio (`int`)
        - mes_fim (`int`)
        - ano_fim (`int`)
        - nome (`str`)

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
