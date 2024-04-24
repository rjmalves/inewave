from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (  # noqa
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.viol_eletricasin import ViolEeletricasinAnos


class ViolEletricasin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à violação das
    restrições elétricas para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `viol_eletricasin.out`.

    """

    BLOCKS = [
        ViolEeletricasinAnos,
    ]
