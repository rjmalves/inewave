from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.cviol_rhv_sin import CviolRhvsinAnos


class CviolRhvsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao custo de violação
    de RHV para o SIN

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `cviol_rhv_sin.out`.

    """

    BLOCKS = [
        CviolRhvsinAnos,
    ]
