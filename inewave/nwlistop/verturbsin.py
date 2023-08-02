from inewave.nwlistop.modelos.verturbsin import VertAnos
from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Verturbsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes às energias
    vertidas para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `verturbsin.out`.

    """

    BLOCKS = [
        VertAnos,
    ]
