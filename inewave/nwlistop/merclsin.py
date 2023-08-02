from inewave.nwlistop.modelos.merclsin import MerclAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Merclsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao mercado líquido
    de cada estágio em cada série.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `merclsin.out`.
    """

    BLOCKS = [
        MerclAnos,
    ]
