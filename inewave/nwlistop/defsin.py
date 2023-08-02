from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.defsin import DefAnos


from os.path import join


class Defsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao déficit
    por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `defsinp001.out`.
    """

    BLOCKS = [
        DefAnos,
    ]
