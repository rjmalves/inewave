from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave.nwlistop.modelos.eafbm00 import LeituraEafbM00

import pandas as pd  # type: ignore


class EafbM00(Arquivo):
    """
    Armazena os dados das saídas referentes às energias
    afluentes brutas, por submercado em valores absolutos.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafbm00x.out`, onde x varia conforme o
    submercado em questão.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="eafbm001.out") -> 'EafbM00':
        """
        """
        leitor = LeituraEafbM00(diretorio)
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
        Tabela com as energias alfuentes totais por série e
        por mês/ano de estudo.

         **Retorna**

        `pd.DataFrame`
        """
        return self._blocos[0].dados[1]
