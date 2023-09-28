from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.mevmin import MevminAnos


class Mevmin(ArquivoREE):
    """
    Armazena os dados das saídas referentes à meta de energia de vazão
    mínima por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `mevmin00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        MevminAnos,
    ]
