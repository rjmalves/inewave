from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (  # noqa
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.cviol_eletricasin import CviolEletricasinAnos


class CviolEletricasin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao custo de violação das
    restrições elétricas para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `cviol_eletricasin.out`.

    """

    BLOCKS = [
        CviolEletricasinAnos,
    ]
