from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.ghtotsin import GHAnos


class GhtotSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração hidraulica total
    por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghtotsin.out`.
    """

    BLOCKS = [
        GHAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="ghtotsin.out"
    ) -> "GhtotSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ghtotsin.out"):
        self.write(diretorio, nome_arquivo)
