from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricao import (
    ArquivoRestricao,
)
from inewave.nwlistop.modelos.cviol_rhv import CviolRhvAnos


class CviolRhv(ArquivoRestricao):
    """
    Armazena os dados das saídas referentes ao custo de violação
    de RHV por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cviol_rhvXXX.out`.

    """

    BLOCKS = [
        Restricao,
        CviolRhvAnos,
    ]
