from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.pivarm import PivarmAnos, PivarmAnos_v29_2


class Pivarm(ArquivoUsina):
    """
    Armazena os dados das saídas referentes aos valores da água
    por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `pivarm00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        PivarmAnos_v29_2,
    ]

    VERSIONS = {
        "28.12": [
            Usina,
            PivarmAnos,
        ],
        "29.2": [
            Usina,
            PivarmAnos_v29_2,
        ],
    }
