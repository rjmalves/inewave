from inewave.newave.modelos.term import BlocoTermUTE

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Term(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos dados das
    usinas térmicas.
    """

    T = TypeVar("T")

    SECTIONS = [BlocoTermUTE]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="term.dat") -> "Term":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="term.dat"):
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
        Tabela com configurações e custos das usinas térmicas.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - potencia_instalada (`float`)
        - fator_capacidade_maximo (`float`)
        - teif (`float`)
        - indisponibilidade_programada (`float`)
        - geracao_minima_janeiro (`float`)
        - ...
        - geracao_minima_dezembro (`float`)
        - geracao_minima_demais_anos (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoTermUTE)
        if isinstance(b, BlocoTermUTE):
            return b.data
        return None

    @usinas.setter
    def usinas(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoTermUTE)
        if isinstance(b, BlocoTermUTE):
            b.data = df
