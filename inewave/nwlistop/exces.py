from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.exces import ExcesAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Exces(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes ao excesso de energia
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `exces00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        ExcesAnos,
    ]
