from inewave._utils.arquivo import ArquivoBlocos
from inewave._utils.dadosarquivo import DadosArquivoBlocos
from inewave._utils.escritablocos import EscritaBlocos

from inewave.newave.modelos.clast import LeituraClasT

import pandas as pd  # type: ignore


class ClasT(ArquivoBlocos):
    """
    Armazena os dados de entrada do NEWAVE referentes às classes de
    usinas térmicas.

    **Parâmetros**

    """

    def __init__(self, dados: DadosArquivoBlocos) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="clast.dat") -> "ClasT":
        """ """
        leitor = LeituraClasT(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="clast.dat"):
        """ """
        escritor = EscritaBlocos(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)

    @property
    def usinas(self) -> pd.DataFrame:
        return self._blocos[0].dados

    @usinas.setter
    def usinas(self, d: pd.DataFrame):
        self._blocos[0].dados = d

    @property
    def modificacoes(self) -> pd.DataFrame:
        return self._blocos[1].dados

    @modificacoes.setter
    def modificacoes(self, d: pd.DataFrame):
        self._blocos[1].dados = d
