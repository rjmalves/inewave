from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.qdesviouh import QdesviouhAnos


class Qdesviouh(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes ao desvio de água por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `qdesviouh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        QdesviouhAnos,
    ]
