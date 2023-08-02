from inewave.nwlistop.modelos.earmfsin import EarmAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


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
