from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoreepatamar import (
    ArquivoREEPatamar,
)
from inewave.nwlistop.modelos.ghmax import GHAnos


class Ghmax(ArquivoREEPatamar):
    """
    Armazena os dados das saídas referentes à geração hidraulica máxima
    por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghmax00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        GHAnos,
    ]
