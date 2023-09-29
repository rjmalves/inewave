from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

from inewave.nwlistop.modelos.vmortsin import VmortAnos


class Vmortsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes à energia
    de enchimento de volume morto para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vmortsin.out`.

    """

    BLOCKS = [
        VmortAnos,
    ]
