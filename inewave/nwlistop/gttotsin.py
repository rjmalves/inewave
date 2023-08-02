from inewave.nwlistop.modelos.gttotsin import GTAnos
from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Gttotsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração térmica total
    por patamar, para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `gttotsin.out`.
    """

    BLOCKS = [
        GTAnos,
    ]
