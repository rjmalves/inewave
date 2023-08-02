from inewave.nwlistop.modelos.verturbsin import VertAnos
from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


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
