from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.evertsin import EvertAnos


class EvertSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao vertimento de reservatórios
    , para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `evertsin.out`.

    """

    BLOCKS = [
        EvertAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="evertsin.out"
    ) -> "EvertSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="evertsin.out"):
        self.write(diretorio, nome_arquivo)
