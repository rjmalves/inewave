from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.cmarg import CmargsAnos, CmargsAnos27


class Cmarg(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes aos custos marginais de operação
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cmarg00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        CmargsAnos,
    ]

    VERSIONS = {
        "27": [
            Submercado,
            CmargsAnos27,
        ],
        "29.4.1": [Submercado, CmargsAnos],
    }
