from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.cterm import CtermsAnos
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)


class Cterm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes aos custos de geração térmica
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cterm00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        CtermsAnos,
    ]
