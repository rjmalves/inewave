from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave.nwlistop.modelos.cmarg00med import LeituraCmarg00med

import pandas as pd  # type: ignore


class Cmarg00med(Arquivo):
    """
    Armazena os dados das saídas referentes aos custos marginais de
    operação médios entre os patamares.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cmarg00x-med.out`, onde x varia conforme o
    submercado em questão.
    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="cmarg001-med.out") -> 'Cmarg00med':
        """
        """
        leitor = LeituraCmarg00med(diretorio)
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
        Tabela com os custos marginais de operação por série
        e por ano/mês de estudo.

         **Retorna**

        `pd.DataFrame`
        """
        return self._blocos[0].dados[1]
