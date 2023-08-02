from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.evertsin import EvertAnos


class Evertsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao vertimento de reservatórios
    , para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `evertsin.out`.

    """

    BLOCKS = [
        EvertAnos,
    ]
