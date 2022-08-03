from inewave.nwlistop.modelos.eafbsin import EafsAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class EafbSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes à energia natural
    afluente para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafbsin.out`.
    """

    BLOCKS = [
        EafsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="eafbsin.out"
    ) -> "EafbSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="eafbsin.out"):
        self.write(diretorio, nome_arquivo)
