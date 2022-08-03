from inewave.nwlistop.modelos.earmfsin import EarmAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class EarmfSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes à energia armazenada
    final em MWmes para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafmfsin.out`.
    """

    BLOCKS = [
        EarmAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="earmfsin.out"
    ) -> "EarmfSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="earmfsin.out"):
        self.write(diretorio, nome_arquivo)
