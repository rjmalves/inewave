from inewave._utils.arquivo import ArquivoBlocos
from inewave._utils.dadosarquivo import DadosArquivoBlocos
from inewave._utils.escritablocos import EscritaBlocos

from inewave.newave.modelos.cvar import LeituraCVAR

from typing import List
import pandas as pd  # type: ignore


class CVAR(ArquivoBlocos):
    """
    Armazena os dados de entrada do NEWAVE referentes ao mecanismo de
    aversão a risco CVAR.

    **Parâmetros**

    """

    def __init__(self, dados: DadosArquivoBlocos) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="cvar.dat") -> "CVAR":
        """ """
        leitor = LeituraCVAR(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="cvar.dat"):
        """ """
        escritor = EscritaBlocos(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)

    @property
    def valores_constantes(self) -> List[float]:
        return self._blocos[0].dados

    @valores_constantes.setter
    def valores_constantes(self, d: List[float]):
        self._blocos[0].dados = d

    @property
    def alfa_variavel(self) -> pd.DataFrame:
        return self._blocos[1].dados

    @alfa_variavel.setter
    def alfa_variavel(self, d: pd.DataFrame):
        self._blocos[1].dados = d

    @property
    def lambda_variavel(self) -> pd.DataFrame:
        return self._blocos[2].dados

    @lambda_variavel.setter
    def lambda_variavel(self, d: pd.DataFrame):
        self._blocos[2].dados = d
