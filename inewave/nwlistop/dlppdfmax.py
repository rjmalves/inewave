from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoreepatamar import (
    ArquivoREEPatamar,
)
from inewave.nwlistop.modelos.dlppdfmax import DLPPdfmaxAnos


class DLPPdfmax(ArquivoREEPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições LPP
    de defluência máxima por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dlppdfmax00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        DLPPdfmaxAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dlppdfmax001.out"
    ) -> "DLPPdfmax":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="dlppdfmax001.out"):
        self.write(diretorio, nome_arquivo)
