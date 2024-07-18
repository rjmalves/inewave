from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricaopatamar import (
    ArquivoRestricaoPatamar,
)
from inewave.nwlistop.modelos.cviol_eletrica import CviolEletricaAnos


class CviolEletrica(ArquivoRestricaoPatamar):
    """
    Armazena os dados das saídas referentes ao custo de violação
    de Restrição Elétrica Especial por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cviol_eletricaXXX.out`.

    """

    BLOCKS = [
        Restricao,
        CviolEletricaAnos,
    ]
