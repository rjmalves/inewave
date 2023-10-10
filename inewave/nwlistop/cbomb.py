from inewave.nwlistop.modelos.blocos.estacaobombeamento import (
    EstacaoBombeamento,
)
from inewave.nwlistop.modelos.arquivos.arquivoestacaobombeamentopatamar import (  # noqa
    ArquivoEstacaoBombeamentoPatamar,
)
from inewave.nwlistop.modelos.cbomb import CBombAnos


class Cbomb(ArquivoEstacaoBombeamentoPatamar):
    """
    Armazena os dados das saídas referentes ao consumo de energia para
    bombeamento por estação.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cbombXXX.out`.

    """

    BLOCKS = [
        EstacaoBombeamento,
        CBombAnos,
    ]
