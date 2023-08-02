from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.verturbm import VertAnos


class Verturbm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às energias
    vertidas, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vertub00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        Submercado,
        VertAnos,
    ]
