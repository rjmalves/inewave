from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricaopatamar import (
    ArquivoRestricaoPatamar,
)
from inewave.nwlistop.modelos.viol_rhq import ViolRHQAnos


class ViolRHQ(ArquivoRestricaoPatamar):
    """
    Armazena os dados das saídas referentes aos valores das restrições
    RHQ por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_rhqXXX.out`.

    """

    BLOCKS = [
        Restricao,
        ViolRHQAnos,
    ]
