from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.ghtotsin import GHAnos


class Ghtotsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração hidraulica total
    por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghtotsin.out`.
    """

    BLOCKS = [
        GHAnos,
    ]
