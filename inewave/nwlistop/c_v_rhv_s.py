from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.c_v_rhv_s import CVRHVAnos

from warnings import warn


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

    def __init__(self, data=...) -> None:
        warn(
            "Esta classe é relativa a um arquivo que não é mais suportado."
            + " Utilize a classe CviolRhvsin no lugar.",
            DeprecationWarning,
        )
        super().__init__(data)
