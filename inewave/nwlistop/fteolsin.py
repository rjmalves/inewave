from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.exces import ExcesAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


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
