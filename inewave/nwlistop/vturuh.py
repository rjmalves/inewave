from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.vturuh import VturAnos

from warnings import warn


class Vturuh(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes às vazões turbinadas por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vturuh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        VturAnos,
    ]

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe Qturuh no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
