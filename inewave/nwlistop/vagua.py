from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.vagua import VAAnos


class Vagua(ArquivoREE):
    """
    Armazena os dados das saídas referentes aos valores da água
    por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vagua00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        VAAnos,
    ]
