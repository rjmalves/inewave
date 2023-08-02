from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.corteolm import CorteolmAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Corteolm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes ao corte de geração eólica.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `corteolm00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Submercado,
        CorteolmAnos,
    ]
