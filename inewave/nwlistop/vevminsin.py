from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.vevminsin import VevminAnos


class VevminSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes às violações da meta
    de energia da vazão mínima para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vevminsin.out`

    """

    BLOCKS = [
        VevminAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vevminsin.out"
    ) -> "VevminSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vevminsin.out"):
        self.write(diretorio, nome_arquivo)
