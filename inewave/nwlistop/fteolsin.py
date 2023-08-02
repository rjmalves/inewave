from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.exces import ExcesAnos


class Fteolsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à folga da variável de
    geração eólica para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `fteolsin.out`

    """

    BLOCKS = [
        ExcesAnos,
    ]
