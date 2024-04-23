from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.viol_ghminm import ViolGhminmAnos


class ViolGhminm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à violação da meta de geração
    hidráulica mínima por patamar, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_ghminm00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        ViolGhminmAnos,
    ]
