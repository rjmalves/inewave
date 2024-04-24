from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.c_v_rhq_s import CVRHQAnos

from warnings import warn


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

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe CviolRhqsin no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
