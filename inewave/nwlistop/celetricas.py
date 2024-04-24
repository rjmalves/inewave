from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (  # noqa
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.celetricas import CeletricasAnos

from warnings import warn


class Celetricas(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao custo de violação das
    restrições elétricas para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `celetricas.out`.

    """

    BLOCKS = [
        CeletricasAnos,
    ]

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe CviolEletricasin no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
