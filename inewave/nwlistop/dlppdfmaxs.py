from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.dlppdfmaxs import DLPPdfmaxAnos


class Dlppdfmaxs(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições
    LPP de defluência máxima por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dlppdfmaxs.out`.
    """

    BLOCKS = [
        DLPPdfmaxAnos,
    ]
