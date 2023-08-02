from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.ghmaxrsin import GHAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Ghmaxrsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração hidraulica máxima
    considerando restrições elétricas por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghmaxsin.out`.
    """

    BLOCKS = [
        GHAnos,
    ]
