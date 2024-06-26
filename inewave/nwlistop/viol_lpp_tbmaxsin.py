from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.viol_lpp_tbmaxsin import ViolLppTbmaxsinAnos


class ViolLppTbmaxsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições
    LPP de turbinamento máximo por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `viol_lpp_tbmaxsin.out`.
    """

    BLOCKS = [
        ViolLppTbmaxsinAnos,
    ]
