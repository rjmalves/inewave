from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.arquivos.arquivorestricaopatamar import (
    ArquivoRestricaoPatamar,
)
from inewave.nwlistop.modelos.viol_eletrica import ViolEletricaAnos


class ViolEletrica(ArquivoRestricaoPatamar):
    """
    Armazena os dados das saídas referentes à violação
    de Restrição Elétrica Especial por restrição.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_eletricaXXX.out`.

    """

    BLOCKS = [
        Restricao,
        ViolEletricaAnos,
    ]
