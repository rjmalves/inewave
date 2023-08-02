from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.vevminsin import VevminAnos


class Vevminsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes às violações da meta
    de energia da vazão mínima para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vevminsin.out`

    """

    BLOCKS = [
        VevminAnos,
    ]
