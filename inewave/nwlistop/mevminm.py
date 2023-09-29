from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)

from inewave.nwlistop.modelos.mevminm import MevminAnos


class Mevminm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes à meta de energia
    de vazão mínima por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `mevminm00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        MevminAnos,
    ]
