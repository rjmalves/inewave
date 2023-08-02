from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE
from inewave.nwlistop.modelos.invade import InvadeAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Invade(ArquivoREE):
    """
    Armazena os dados das saídas referentes às violações da CAR
    , por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `invade00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        InvadeAnos,
    ]
