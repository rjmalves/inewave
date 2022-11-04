from inewave.nwlistop.modelos.merclsin import MerclAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class MerclSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao mercado líquido
    de cada estágio em cada série.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `merclsin.out`.
    """

    BLOCKS = [
        MerclAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="merclsin.out"
    ) -> "MerclSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="merclsin.out"):
        self.write(diretorio, nome_arquivo)
