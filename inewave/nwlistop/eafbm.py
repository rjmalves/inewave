from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.eafbm import EafsAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Eafbm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às energias
    afluentes brutas, por submercado em valores absolutos.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafbm00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        EafsAnos,
    ]
