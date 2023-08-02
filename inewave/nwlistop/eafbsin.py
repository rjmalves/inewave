from inewave.nwlistop.modelos.eafbsin import EafsAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Eafbsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes à energia natural
    afluente para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafbsin.out`.
    """

    BLOCKS = [
        EafsAnos,
    ]
