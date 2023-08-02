from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.dfphauh import DfphauhAnos


class Dfphauh(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à variável de folga da
    FPHA da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dfphauh00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        DfphauhAnos,
    ]
