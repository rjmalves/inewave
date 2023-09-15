from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.hmont import HmontAnos


class Hmont(ArquivoUsina):
    """
    Armazena os dados das saídas referentes à cota de montante por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `hmont00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        HmontAnos,
    ]
