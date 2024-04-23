from inewave.nwlistop.modelos.blocos.estacaobombeamento import (
    EstacaoBombeamento,
)
from inewave.nwlistop.modelos.arquivos.arquivoestacaobombeamentopatamar import (  # noqa
    ArquivoEstacaoBombeamentoPatamar,
)
from inewave.nwlistop.modelos.qbomb import QBombAnos


class Qbomb(ArquivoEstacaoBombeamentoPatamar):
    """
    Armazena os dados das saídas referentes à vazão bombeada
    por estação de bombeamento.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `qbombXXX.out`.

    """

    BLOCKS = [
        EstacaoBombeamento,
        QBombAnos,
    ]
