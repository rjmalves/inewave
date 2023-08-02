from inewave.nwlistop.modelos.merclsin import MerclAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class Merclsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao mercado líquido
    de cada estágio em cada série.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `merclsin.out`.
    """

    BLOCKS = [
        MerclAnos,
    ]
