from inewave.nwlistop.modelos.cdefsin import CdefAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class Cdefsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao custo de déficit
    de cada estágio em cada série.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cdefsin.out`.
    """

    BLOCKS = [
        CdefAnos,
    ]
