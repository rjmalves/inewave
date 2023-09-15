from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.desvuh import DesvuhAnos


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
