from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.c_v_rhq_s import CVRHQAnos


class CVRHQs(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao custo de violação
    de RHQ para o SIN

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `c_v_rhq_s.out`.

    """

    BLOCKS = [
        CVRHQAnos,
    ]
