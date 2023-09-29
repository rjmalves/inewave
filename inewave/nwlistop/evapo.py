from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.evapo import EvapoAnos


class Evapo(ArquivoREE):
    """
    Armazena os dados das saídas referentes à energia evaporada
    por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `evapo00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        EvapoAnos,
    ]
