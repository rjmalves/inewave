from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.cviol_rhq_sin import CviolRhqsinAnos


class CviolRhqsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao custo de violação
    de RHQ para o SIN

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `cviol_rhq_sin.out`.

    """

    BLOCKS = [
        CviolRhqsinAnos,
    ]
