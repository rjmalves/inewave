from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.perdfm import PerdfAnos


class Perdfm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes ao vertimento fio d'água
    , por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `perdfm00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        PerdfAnos,
    ]
