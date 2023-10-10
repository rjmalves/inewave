from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (  # noqa
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.cbombsin import CBombAnos


class Cbombsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao consumo de energia para
    bombeamento para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `cbombsin.out`.

    """

    BLOCKS = [
        CBombAnos,
    ]
