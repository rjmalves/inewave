from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivoclassetermicasubmercadopatamar import (
    ArquivoClasseTermicaSubmercadoPatamar,
)
from inewave.nwlistop.modelos.gtert import GTAnos


class Gtert(ArquivoClasseTermicaSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à geração térmica por classe
    térmica, por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `gtert00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        GTAnos,
    ]
