from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.vghminm import VghminAnos

from warnings import warn


class Vghminm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à violação da meta de geração
    hidráulica mínima por patamar, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vghmin00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        VghminAnos,
    ]

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe ViolGhminm no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
