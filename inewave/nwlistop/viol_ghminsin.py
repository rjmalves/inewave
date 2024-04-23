from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.viol_ghminsin import ViolGhminsinAnos


class ViolGhminsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à violação da meta de geração
    hidraulica mínima por patamar, para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `viol_ghminsin.out`.

    """

    BLOCKS = [
        ViolGhminsinAnos,
    ]
