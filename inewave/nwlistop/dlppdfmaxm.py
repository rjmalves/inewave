from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.dlppdfmax import DLPPdfmaxAnos


class Dlppdfmaxm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições LPP
    de defluência máxima por patamar, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dlppdfmax00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        DLPPdfmaxAnos,
    ]
