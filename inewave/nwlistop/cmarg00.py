from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave.nwlistop.modelos.cmarg00 import LeituraCmarg00

import pandas as pd  # type: ignore


class Cmarg00(Arquivo):
    """
    Armazena os dados das saídas referentes aos custos marginais de operação
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cmarg00x.out`, onde x varia conforme o
    submercado em questão.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="cmarg001.out") -> 'Cmarg00':
        """
        """
        leitor = LeituraCmarg00(diretorio)
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
    def custos(self) -> pd.DataFrame:
        """
        Tabela com os custos marginais por patamar, por série e
        por mês/ano de estudo.

         **Retorna**

        `pd.DataFrame`
        """
        return self._blocos[0].dados[1]
