from inewave.newave.modelos.patamar import (
    BlocoNumeroPatamares,
    BlocoDuracaoPatamar,
    BlocoCargaPatamar,
    BlocoIntercambioPatamarSubsistemas,
    BlocoUsinasNaoSimuladas,
)

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Patamar(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos
    patamares de carga por submercado.

    """

    T = TypeVar("T")

    SECTIONS = [
        BlocoNumeroPatamares,
        BlocoDuracaoPatamar,
        BlocoCargaPatamar,
        BlocoIntercambioPatamarSubsistemas,
        BlocoUsinasNaoSimuladas,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="patamar.dat"
    ) -> "Patamar":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="patamar.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def numero_patamares(self) -> Optional[int]:
        """
        O número de patamares utilizado no estudo.

        :return: O número de patamares como um inteiro
        :rtype: int | None
        """
        b = self.data.get_sections_of_type(BlocoNumeroPatamares)
        if isinstance(b, BlocoNumeroPatamares):
            return b.data
        return None

    @numero_patamares.setter
    def numero_patamares(self, n: int):
        b = self.data.get_sections_of_type(BlocoNumeroPatamares)
        if isinstance(b, BlocoNumeroPatamares):
            b.data = n

    @property
    def duracao_mensal_patamares(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a duração mensal de cada patamar no horizonte
        de estudo.

        - ano (`int`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: A duração por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoDuracaoPatamar)
        if isinstance(b, BlocoDuracaoPatamar):
            return b.data
        return None

    @duracao_mensal_patamares.setter
    def duracao_mensal_patamares(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoDuracaoPatamar)
        if isinstance(b, BlocoDuracaoPatamar):
            b.data = df

    @property
    def carga_patamares(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a carga em P.U. por patamar.

        - ano (`int`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: A carga por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoCargaPatamar)
        if isinstance(b, BlocoCargaPatamar):
            return b.data
        return None

    @carga_patamares.setter
    def carga_patamares(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoCargaPatamar)
        if isinstance(b, BlocoCargaPatamar):
            b.data = df

    @property
    def intercambio_patamares(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a correção em P.U. do intercâmbio por patamar.

        - submercado_de (`str`)
        - submercado_para (`str`)
        - ano (`int`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: A carga por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoIntercambioPatamarSubsistemas)
        if isinstance(b, BlocoIntercambioPatamarSubsistemas):
            return b.data
        return None

    @intercambio_patamares.setter
    def intercambio_patamares(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoIntercambioPatamarSubsistemas)
        if isinstance(b, BlocoIntercambioPatamarSubsistemas):
            b.data = df

    @property
    def usinas_nao_simuladas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os fatores das usinas não simuladas em P.U.

        - submercado (`int`)
        - patamar (`int`)
        - bloco (`int`)
        - ano (`int`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: Os valores por mês em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoUsinasNaoSimuladas)
        if isinstance(b, BlocoUsinasNaoSimuladas):
            return b.data
        return None

    @usinas_nao_simuladas.setter
    def usinas_nao_simuladas(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoUsinasNaoSimuladas)
        if isinstance(b, BlocoUsinasNaoSimuladas):
            b.data = df
