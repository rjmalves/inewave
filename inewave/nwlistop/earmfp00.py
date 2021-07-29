from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave.nwlistop.modelos.earmfp00 import LeituraEarmfp00

import pandas as pd  # type: ignore


class Earmfp00(Arquivo):
    """
    Armazena os dados das saídas referentes às armazenadas finais,
    por REE em valores absolutos.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `earmfp00x.out`, onde x varia conforme o
    REE em questão.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="earmfp001.out") -> 'Earmfp00':
        """
        """
        leitor = LeituraEarmfp00(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    @property
    def ree(self) -> str:
        """
        Tabela com o REE associado ao arquivo lido.

         **Retorna**

        `str`
        """
        return self._blocos[0].dados[0]

    @property
    def energias(self) -> pd.DataFrame:
        """
        Tabela com as energias armazenadas finais por série e
        por mês/ano de estudo.

         **Retorna**

        `pd.DataFrame`
        """
        return self._blocos[0].dados[1]
