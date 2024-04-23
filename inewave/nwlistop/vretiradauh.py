from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.vretiradauh import VretiradauhAnos


class Vretiradauh(ArquivoUsina):
    """
    Armazena os dados das saídas referentes à retirada de água por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vretiradauh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        VretiradauhAnos,
    ]
