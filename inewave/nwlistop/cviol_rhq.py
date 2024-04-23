from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricaopatamar import (
    ArquivoRestricaoPatamar,
)
from inewave.nwlistop.modelos.cviol_rhq import CviolRhqAnos


class CviolRhq(ArquivoRestricaoPatamar):
    """
    Armazena os dados das saídas referentes ao custo de violação
    de RHQ por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cviol_rhqXXX.out`.

    """

    BLOCKS = [
        Restricao,
        CviolRhqAnos,
    ]
