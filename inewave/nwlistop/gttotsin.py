from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave.nwlistop.modelos.gttotsin import LeituraGTTotSIN

import pandas as pd  # type: ignore


class GTTotSIN(Arquivo):
    """
    Armazena os dados das saídas referentes à geração térmica total
    por patamar, para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `gttotsin.out`.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="gttotsin.out") -> 'GTTotSIN':
        """
        """
        leitor = LeituraGTTotSIN(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    @property
    def geracao(self) -> pd.DataFrame:
        """
        Tabela com a geração térmica por patamar, por série e
        por mês/ano de estudo.

         **Retorna**

        `pd.DataFrame`
        """
        return self._blocos[0].dados
