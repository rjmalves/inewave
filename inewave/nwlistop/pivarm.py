from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.pivarm import PivarmAnos


class Pivarm(ArquivoUsina):
    """
    Armazena os dados das saídas referentes aos valores da água
    por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `pivarm00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        PivarmAnos,
    ]
