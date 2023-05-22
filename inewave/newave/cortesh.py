from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.cortesh import SecaoDadosCortesH
import pandas as pd  # type: ignore


from typing import TypeVar, Optional

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class CortesH(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes ao
    cabeçalho dos cortes de Benders.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosCortesH]
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__df: Optional[pd.DataFrame] = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="cortesh.dat"
    ) -> "CortesH":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="cortesh.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def dados(self) -> Optional[SecaoDadosCortesH]:
        dados = [r for r in self.data.of_type(SecaoDadosCortesH)]
        if len(dados) == 1:
            return dados[0]
        else:
            return None
