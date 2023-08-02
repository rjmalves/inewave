from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.perdfsin import PerdfAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


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
