from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricao import (
    ArquivoRestricao,
)
from inewave.nwlistop.modelos.c_v_rhv import CVRHVAnos


class CVRHV(ArquivoRestricao):
    """
    Armazena os dados das saídas referentes ao custo de violação
    de RHV por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `c_v_rhvXXX.out`.

    """

    BLOCKS = [
        Restricao,
        CVRHVAnos,
    ]
