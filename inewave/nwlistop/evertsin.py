from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.evertsin import EvertAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


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
