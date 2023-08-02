from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoreepatamar import (
    ArquivoREEPatamar,
)
from inewave.nwlistop.modelos.rhslppdf import RHSLPPdfAnos


class Rhslppdf(ArquivoREEPatamar):
    """
    Armazena os dados das saídas referentes ao RHS das restrições LPP
    de defluência máxima por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `rhslppdf00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        RHSLPPdfAnos,
    ]
