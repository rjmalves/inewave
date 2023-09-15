from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.hjus import HjusAnos


class Hjus(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à cota de jusante por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `hjus00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        HjusAnos,
    ]
