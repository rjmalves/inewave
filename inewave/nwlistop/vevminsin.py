from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.vevminsin import VevminAnos

from warnings import warn


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

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe ViolEvminsin no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
