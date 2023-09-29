from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.vmort import VmortAnos


class Vmort(ArquivoREE):
    """
    Armazena os dados das saídas referentes à energia de enchimento
    de volume morto por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `mort00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        VmortAnos,
    ]
