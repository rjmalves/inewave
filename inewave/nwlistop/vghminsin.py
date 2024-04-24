from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.vghmin import VghminAnos

from warnings import warn


class Vghminsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à violação da meta de geração
    hidraulica mínima por patamar, para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `vghminsin.out`.

    """

    BLOCKS = [
        VghminAnos,
    ]

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe ViolGhminsin no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
