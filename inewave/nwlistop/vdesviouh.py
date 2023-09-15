from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.vdesviouh import VdesviouhAnos


class Vdesviouh(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes ao desvio de água por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vdesviouh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        VdesviouhAnos,
    ]
