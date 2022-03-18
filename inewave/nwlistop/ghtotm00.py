from inewave._utils.dadosarquivo import DadosArquivoBlocos
from inewave._utils.arquivo import ArquivoBlocos
from inewave.nwlistop.modelos.ghtotm00 import LeituraGHTotM00

import pandas as pd  # type: ignore


class GHTotM00(ArquivoBlocos):
    """
    Armazena os dados das saídas referentes à geração hidraulica total
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghtotm00x.out`, onde x varia conforme o
    submercado em questão.

    """

    def __init__(self, dados: DadosArquivoBlocos):
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="ghtotm001.out"
    ) -> "GHTotM00":
        """ """
        leitor = LeituraGHTotM00(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    @property
    def submercado(self) -> str:
        """
        Tabela com o submercado associado ao arquivo lido.

         **Retorna**

        `str`
        """
        return self._blocos[0].dados[0]

    @property
    def geracao(self) -> pd.DataFrame:
        """
        Tabela com a geração hidraulica por patamar, por série e
        por mês/ano de estudo.

         **Retorna**

        `pd.DataFrame`
        """
        return self._blocos[0].dados[1]
