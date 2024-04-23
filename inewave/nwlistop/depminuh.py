from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.depminuh import DepminAnos

from warnings import warn


class Depminuh(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes À violação de defluência
    mínima da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `depminuh00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        DepminAnos,
    ]

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe ViolVazmin no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
