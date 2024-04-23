from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.desvuh import DesvuhAnos

from warnings import warn


class Desvuh(ArquivoUsina):
    """
    Armazena os dados das saídas referentes à retirada de água por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `desvuh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        DesvuhAnos,
    ]

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe Vretiradauh no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
