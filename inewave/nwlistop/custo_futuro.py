from inewave.nwlistop.modelos.custo_futuro import CustoFuturoAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class CustoFuturo(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao custo futuro
    de cada estágio em cada série.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `custo_futuro.out`.
    """

    BLOCKS = [
        CustoFuturoAnos,
    ]
