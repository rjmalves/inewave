from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.escrita import Escrita
from inewave.newave.modelos.adterm import LeituraAdTerm

import pandas as pd  # type: ignore


class AdTerm(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes às térmicas de
    despacho antecipado disponíveis.

    **Parâmetros**

    """

    def __init__(self,
                 dados: DadosArquivo) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="adterm.dat") -> 'AdTerm':
        """
        """
        leitor = LeituraAdTerm(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="adterm.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)

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
