from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.c_v_rhv_s import CVRHVAnos


class CVRHVs(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao custo de violação
    de RHV para o SIN

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `c_v_rhv_s.out`.

    """

    BLOCKS = [
        CVRHVAnos,
    ]
