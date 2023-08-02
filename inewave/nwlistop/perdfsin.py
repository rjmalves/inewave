from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.perdfsin import PerdfAnos


class Perdfsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao vertimento fio d'água
    , para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `perdfsin.out`.

    """

    BLOCKS = [
        PerdfAnos,
    ]
