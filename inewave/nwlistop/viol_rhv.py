from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricao import (
    ArquivoRestricao,
)
from inewave.nwlistop.modelos.viol_rhv import ViolRHVAnos


class ViolRHV(ArquivoRestricao):
    """
    Armazena os dados das saídas referentes aos valores das violações
    das restrições RHV por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_rhvXXX.out`.

    """

    BLOCKS = [
        Restricao,
        ViolRHVAnos,
    ]
