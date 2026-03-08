from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.dtbmin import DtbminAnos

from warnings import warn
from typing import Any


class Dtbmin(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à violação de restrição de
    turbinamento mínimo por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dtbmin00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        DtbminAnos,
    ]

    def __init__(self, data: Any = ...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe ViolTurbmin no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
