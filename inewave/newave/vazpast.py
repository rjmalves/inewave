from inewave.newave.modelos.vazpast import BlocoVazPast

from cfinterface.files.sectionfile import SectionFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Vazpast(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às
    vazões anteriores ao período de planejamento.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que são usadas juntos das contidas no arquivo `vazoes.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoVazPast]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vazpast.dat"
    ) -> "Vazpast":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vazpast.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def tendencia(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a tendência hidrológica por UHE.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - janeiro (`float`)
        - ...
        - dezembro (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(BlocoVazPast)
        if isinstance(b, BlocoVazPast):
            return b.data
        return None

    @tendencia.setter
    def tendencia(self, df: pd.DataFrame):
        b = self.data.get_sections_of_type(BlocoVazPast)
        if isinstance(b, BlocoVazPast):
            b.data = df
