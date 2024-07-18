from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.viol_pos_vretiruh import ViolPosVretiruhAnos


class ViolPosVretiruh(ArquivoUsina):
    """
    Armazena os dados das saídas referentes ao desvios positivos da
    retirada de água da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_pos_vretiruhXXX.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        ViolPosVretiruhAnos,
    ]
