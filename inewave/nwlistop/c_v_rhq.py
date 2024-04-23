from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricaopatamar import (
    ArquivoRestricaoPatamar,
)
from inewave.nwlistop.modelos.c_v_rhq import CVRHQAnos

from warnings import warn


class CVRHQ(ArquivoRestricaoPatamar):
    """
    Armazena os dados das saídas referentes ao custo de violação
    de RHQ por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `c_v_rhqXXX.out`.

    """

    BLOCKS = [
        Restricao,
        CVRHQAnos,
    ]

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe CviolRhq no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
