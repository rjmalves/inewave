from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.viol_neg_vretiruh import ViolNegVretiruhAnos


class ViolNegVretiruh(ArquivoUsina):
    """
    Armazena os dados das saídas referentes ao desvios negativos da
    retirada de água da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_neg_vretiruhXXX.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        ViolNegVretiruhAnos,
    ]
