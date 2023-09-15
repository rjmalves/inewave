from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.hliq import HliqAnos


class Hliq(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à queda líquida por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `hliq00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        HliqAnos,
    ]
