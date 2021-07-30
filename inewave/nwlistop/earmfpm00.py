from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave.nwlistop.modelos.earmfpm00 import LeituraEarmfpM00

import pandas as pd  # type: ignore


class EarmfpM00(Arquivo):
    """
    Armazena os dados das saídas referentes às energias
    armazenadas finais, por submercado e em % da energia armazenável máxima.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `earmfpm00x.out`, onde x varia conforme o
    submercado em questão.
    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="earmfpm001.out") -> 'EarmfpM00':
        """
        """
        leitor = LeituraEarmfpM00(diretorio)
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
    def energias(self) -> pd.DataFrame:
        """
        Tabela com as energias armazenadas percentuais por série e
        por mês/ano de estudo.

         **Retorna**

        `pd.DataFrame`
        """
        return self._blocos[0].dados[1]
