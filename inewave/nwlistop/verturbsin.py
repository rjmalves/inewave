from inewave.nwlistop.modelos.verturbsin import VertAnos
from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class VerturbSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes às energias
    vertidas para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `verturbsin.out`.

    """

    BLOCKS = [
        VertAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="verturbsin.out"
    ) -> "VerturbSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="verturbsin.out"):
        self.write(diretorio, nome_arquivo)
