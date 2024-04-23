from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (  # noqa
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.deletricas import DeletricasAnos

from warnings import warn


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

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe ViolEletricas no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
