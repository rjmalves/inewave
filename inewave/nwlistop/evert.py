from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE
from inewave.nwlistop.modelos.evert import EvertAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Evert(ArquivoREE):
    """
    Armazena os dados das saídas referentes ao vertimento de reservatórios
    , por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `evert00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        EvertAnos,
    ]
