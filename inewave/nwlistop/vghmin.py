from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoreepatamar import (
    ArquivoREEPatamar,
)
from inewave.nwlistop.modelos.vghmin import VghminAnos

from warnings import warn


class Vghmin(ArquivoREEPatamar):
    """
    Armazena os dados das saídas referentes à violação da meta de geração
    hidraulica mínima por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vghmin00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        VghminAnos,
    ]

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe ViolGhmin no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
