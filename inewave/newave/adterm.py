from inewave._utils.arquivo import ArquivoBlocos
from inewave._utils.dadosarquivo import DadosArquivoBlocos
from inewave._utils.escritablocos import EscritaBlocos

from inewave.newave.modelos.adterm import LeituraAdTerm

import pandas as pd  # type: ignore


class AdTerm(ArquivoBlocos):
    """
    Armazena os dados de entrada do NEWAVE referentes às térmicas de
    despacho antecipado disponíveis.

    **Parâmetros**

    """

    def __init__(self, dados: DadosArquivoBlocos) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="adterm.dat") -> "AdTerm":
        """ """
        leitor = LeituraAdTerm(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="adterm.dat"):
        """ """
        escritor = EscritaBlocos(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)

    @property
    def despachos(self) -> pd.DataFrame:
        """
        Despachos antecipados das térmicas GNL.

        **Retorna**

        `pd.DataFrame`

        """
        return self._blocos[0].dados

    @despachos.setter
    def despachos(self, term: pd.DataFrame):
        self._blocos[0].dados = term
