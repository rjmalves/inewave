from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.viol_pos_evap import ViolPosEvapAnos


class ViolPosEvap(ArquivoUsina):
    """
    Armazena os dados das saídas referentes ao desvios positivos da
    evaporação da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_pos_evap00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        ViolPosEvapAnos,
    ]
