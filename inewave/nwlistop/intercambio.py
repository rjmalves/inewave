from inewave.nwlistop.modelos.blocos.parsubmercados import ParSubmercados
from inewave.nwlistop.modelos.arquivos.arquivoparsubmercadopatamar import (
    ArquivoParSubmercadoPatamar,
)
from inewave.nwlistop.modelos.intercambio import IntercambioAnos


class Intercambio(ArquivoParSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes ao intercâmbio
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `int00x00y.out`, onde x e y variam
    conforme os submercados em questão.

    """

    BLOCKS = [
        ParSubmercados,
        IntercambioAnos,
    ]
