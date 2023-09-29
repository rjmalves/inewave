from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)

from inewave.nwlistop.modelos.vmortm import VmortAnos


class Vmortm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes à energia
    de enchimento de volume morto por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vmortm00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        VmortAnos,
    ]
