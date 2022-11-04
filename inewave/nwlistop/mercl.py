from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.merclsin import MerclAnos

from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)


class Mercl(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes ao mercado líquido
    de cada estágio em cada série por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `mercl001.out`.
    """

    BLOCKS = [
        Submercado,
        MerclAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="mercl001.out"
    ) -> "Mercl":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="mercl001.out"):
        self.write(diretorio, nome_arquivo)
