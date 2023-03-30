from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.dfphauh import DfphauhAnos


class Dfphauh(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à variável de folga da
    FPHA da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dfphauh00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        DfphauhAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dfphauh001.out"
    ) -> "Dfphauh":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="dfphauh001.out"):
        self.write(diretorio, nome_arquivo)
