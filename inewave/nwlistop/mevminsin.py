from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

from inewave.nwlistop.modelos.mevminsin import MevminAnos


class Mevminsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes à meta de energia
    de vazão mínima para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `mevminsin.out`.

    """

    BLOCKS = [
        MevminAnos,
    ]
