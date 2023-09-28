from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

from inewave.nwlistop.modelos.edesvcsin import EdesvcsinAnos


class Edesvcsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes às energias
    de desvio de água controlável para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `edesvcsin.out`.

    """

    BLOCKS = [
        EdesvcsinAnos,
    ]
