from inewave.nwlistop.modelos.ctermsin import CtermsAnos
from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


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
