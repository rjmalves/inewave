from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.geolm import GEAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Geolm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à geração eólica total
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `geol00x.out`, onde x varia conforme o
    PEE em questão.

    """

    BLOCKS = [
        Submercado,
        GEAnos,
    ]
