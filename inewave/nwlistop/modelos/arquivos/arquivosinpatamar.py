from inewave.nwlistop.modelos.arquivos._base_serie_patamar import (
    _ArquivoSeriePatamarBase,
)
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class ArquivoSINPatamar(_ArquivoSeriePatamarBase):
    """
    Armazena os dados das saídas por submercado.
    """

    __slots__: list[str] = []

    BLOCKS = [ValoresSeriePatamar]
