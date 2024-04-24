from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.viol_lpp_dfmaxsin import ViolLppDfmaxsinAnos


class ViolLppDfmaxsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições
    LPP de defluência máxima por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_lpp_dfmaxsin.out`.
    """

    BLOCKS = [
        ViolLppDfmaxsinAnos,
    ]
