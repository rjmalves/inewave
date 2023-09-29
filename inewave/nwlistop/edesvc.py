from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.edesvc import EdesvcAnos


class Edesvc(ArquivoREE):
    """
    Armazena os dados das saídas referentes às energias
    de desvio de água controlável por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `edesvc00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        EdesvcAnos,
    ]
