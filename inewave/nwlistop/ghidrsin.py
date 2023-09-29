from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.ghidrsin import GHAnos


class Ghidrsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração hidraulica controlável
    por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghidrsin.out`.
    """

    BLOCKS = [
        GHAnos,
    ]
