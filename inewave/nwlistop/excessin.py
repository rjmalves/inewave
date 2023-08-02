from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.exces import ExcesAnos


class Excessin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao excesso de energia
    por patamar, para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `excessin.out`

    """

    BLOCKS = [
        ExcesAnos,
    ]
