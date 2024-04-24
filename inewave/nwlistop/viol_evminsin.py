from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.viol_evminsin import ViolEvminsinAnos


class ViolEvminsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes às violações da meta
    de energia da vazão mínima para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_evminsin.out`

    """

    BLOCKS = [
        ViolEvminsinAnos,
    ]
