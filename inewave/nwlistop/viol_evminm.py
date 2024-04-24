from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.viol_evminm import ViolEvminmAnos


class ViolEvminm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às violações da meta
    de energia da vazão mínima, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_evminm00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        ViolEvminmAnos,
    ]
