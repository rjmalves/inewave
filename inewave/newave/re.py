from inewave._utils.dadosarquivo import DadosArquivoBlocos
from inewave._utils.arquivo import ArquivoBlocos
from inewave._utils.escritablocos import EscritaBlocos

from inewave.newave.modelos.re import LeituraRE

import pandas as pd  # type: ignore


class RE(ArquivoBlocos):
    """
    Armazena os dados de entrada do NEWAVE referentes às restrições
    elétricas existentes.

    **Parâmetros**

    """

    def __init__(self, dados: DadosArquivoBlocos) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="re.dat") -> "RE":
        """ """
        leitor = LeituraRE(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="re.dat"):
        """ """
        escritor = EscritaBlocos(diretorio)
        escritor.escreve_arquivo(self._dados, nome_arquivo)

    @property
    def usinas_conjuntos(self) -> pd.DataFrame:
        """
        Tabela com os conjuntos de usinas com restrições elétricas.

        **Retorna**

        `pd.DataFrame`

        **Sobre**
        """
        return self._blocos[0].dados

    @usinas_conjuntos.setter
    def usinas_conjuntos(self, conjuntos: pd.DataFrame):
        self._blocos[0].dados = conjuntos

    @property
    def restricoes(self) -> pd.DataFrame:
        """
        Tabela com as configurações das restrições elétricas.

        **Retorna**

        `pd.DataFrame`

        **Sobre**
        """
        return self._blocos[1].dados

    @restricoes.setter
    def restricoes(self, config: pd.DataFrame):
        self._blocos[1].dados = config
