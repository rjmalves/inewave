from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.cmargmed import CmargsAnos, CmargsAnos28


class Cmargmed(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes aos custos marginais de operação
    por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cmarg00x-med.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        CmargsAnos,
    ]

    VERSIONS = {
        "28": [
            Submercado,
            CmargsAnos28,
        ],
        "29.4.1": [Submercado, CmargsAnos],
    }
