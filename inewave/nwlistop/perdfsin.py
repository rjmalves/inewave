from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.perdfsin import PerdfAnos


class PerdfSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao vertimento fio d'água
    , para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `perdfsin.out`.

    """

    BLOCKS = [
        PerdfAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="perdfsin.out"
    ) -> "PerdfSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="perdfsin.out"):
        self.write(diretorio, nome_arquivo)
