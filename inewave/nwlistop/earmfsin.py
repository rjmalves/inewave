from inewave.nwlistop.modelos.earmfsin import EarmAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Earmfsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes à energia armazenada
    final em MWmes para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafmfsin.out`.
    """

    BLOCKS = [
        EarmAnos,
    ]
