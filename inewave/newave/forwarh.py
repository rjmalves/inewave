from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.forwarh import SecaoDadosForwarh
import pandas as pd  # type: ignore


from typing import TypeVar, Optional

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Forwarh(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes ao
    cabeçalho dos dados das simulações forward.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosForwarh]
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="forwarh.dat"
    ) -> "Forwarh":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="forwarh.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    @property
    def dados(self) -> Optional[SecaoDadosForwarh]:
        dados = [r for r in self.data.of_type(SecaoDadosForwarh)]
        if len(dados) == 1:
            return dados[0]
        else:
            return None
