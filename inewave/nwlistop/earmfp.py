from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.earmfp import EarmsAnos


class Earmfp(ArquivoREE):
    """
    Armazena os dados das saídas referentes às energias
    armazenadas finais, por REE e em % da energia armazenável máxima.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `earmfp00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        EarmsAnos,
    ]
