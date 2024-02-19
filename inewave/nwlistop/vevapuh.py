from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.vevapuh import VevapuhAnos


class Vevapuh(ArquivoUsina):
    """
    Armazena os dados das saídas referentes aos volumes evaporados da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vevapuh00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        VevapuhAnos,
    ]
