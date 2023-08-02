from inewave.nwlistop.modelos.coper import CoperAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Coper(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao custo total de operação
    de cada estágio em cada série.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `coper.out`.
    """

    BLOCKS = [
        CoperAnos,
    ]
