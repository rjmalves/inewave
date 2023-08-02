from inewave.nwlistop.modelos.ctermsin import CtermsAnos
from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class Ctermsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes aos custos de geração térmica
    para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ctermsin.out`.

    """

    BLOCKS = [
        CtermsAnos,
    ]
