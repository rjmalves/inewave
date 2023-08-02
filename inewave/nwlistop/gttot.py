from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.gttot import GTAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Gttot(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à geração térmica total
    por patamar, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `gttot00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        GTAnos,
    ]
