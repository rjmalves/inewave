from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoreepatamar import (
    ArquivoREEPatamar,
)
from inewave.nwlistop.modelos.dlpptbmax import DLPPtbmaxAnos


class DLPPtbmax(ArquivoREEPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições LPP
    de turbinamento máximo por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dlpptbmax00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        DLPPtbmaxAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dlpptbmax001.out"
    ) -> "DLPPtbmax":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="dlpptbmax001.out"):
        self.write(diretorio, nome_arquivo)
