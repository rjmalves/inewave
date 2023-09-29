from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)

from inewave.nwlistop.modelos.evapom import EvapoAnos


class Evapom(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes à energia
    de evaporação por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `evapom00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        EvapoAnos,
    ]
