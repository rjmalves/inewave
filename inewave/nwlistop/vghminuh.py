from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.vghminuh import VGhminuhAnos


class Vghminuh(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à violação da meta de
    geração hidráulica mínima por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vghminuh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        VGhminuhAnos,
    ]
