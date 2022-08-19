from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoreepatamar import (
    ArquivoREEPatamar,
)
from inewave.nwlistop.modelos.rhslpptb import RHSLPPtbAnos


class RHSLPPtb(ArquivoREEPatamar):
    """
    Armazena os dados das saídas referentes ao RHS das restrições LPP
    de turbinamento máximo por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `rhslpptb00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        RHSLPPtbAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="rhslpptb001.out"
    ) -> "RHSLPPtb":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="rhslpptb001.out"):
        self.write(diretorio, nome_arquivo)
