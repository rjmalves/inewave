from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave.nwlistop.modelos.ghtotsin import LeituraGHTotSIN

import pandas as pd  # type: ignore


class GHTotSIN(Arquivo):
    """
    Armazena os dados das saídas referentes à geração hidraulica total
    por patamar, para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghtotm00x.out`, onde x varia conforme o
    submercado em questão.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="ghtotsin.out") -> 'GHTotSIN':
        """
        """
        leitor = LeituraGHTotSIN(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    @property
    def geracao(self) -> pd.DataFrame:
        """
        Tabela com a geração hidraulica por patamar, por série e
        por mês/ano de estudo.

         **Retorna**

        `pd.DataFrame`
        """
        return self._blocos[0].dados
