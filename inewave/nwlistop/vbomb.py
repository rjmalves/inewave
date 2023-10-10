from inewave.nwlistop.modelos.blocos.estacaobombeamento import (
    EstacaoBombeamento,
)
from inewave.nwlistop.modelos.arquivos.arquivoestacaobombeamentopatamar import (  # noqa
    ArquivoEstacaoBombeamentoPatamar,
)
from inewave.nwlistop.modelos.vbomb import VBombAnos


class Vbomb(ArquivoEstacaoBombeamentoPatamar):
    """
    Armazena os dados das saídas referentes ao volume bombeado
    por estação de bombeamento.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vbombXXX.out`.

    """

    BLOCKS = [
        EstacaoBombeamento,
        VBombAnos,
    ]
