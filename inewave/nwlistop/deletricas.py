from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (  # noqa
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.deletricas import DeletricasAnos


class Deletricas(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à violação das
    restrições elétricas para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `deletricas.out`.

    """

    BLOCKS = [
        DeletricasAnos,
    ]
