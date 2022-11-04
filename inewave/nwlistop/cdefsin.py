from inewave.nwlistop.modelos.cdefsin import CdefAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class CdefSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao custo de déficit
    de cada estágio em cada série.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cdefsin.out`.
    """

    BLOCKS = [
        CdefAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="cdefsin.out"
    ) -> "CdefSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="cdefsin.out"):
        self.write(diretorio, nome_arquivo)
