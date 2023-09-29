from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

from inewave.nwlistop.modelos.evaporsin import EvapoAnos


class Evaporsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes à energia
    de evaporação para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `evaporsin.out`.

    """

    BLOCKS = [
        EvapoAnos,
    ]
