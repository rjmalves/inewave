from inewave.nwlistop.modelos.gttotsin import GTAnos
from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)


from os.path import join


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
