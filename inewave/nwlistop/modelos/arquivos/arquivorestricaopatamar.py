from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie_patamar import (
    _ArquivoSeriePatamarBase,
)
from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class ArquivoRestricaoPatamar(_ArquivoSeriePatamarBase):
    """
    Armazena os dados das saídas por patamar, por Restrição.
    """

    __slots__: list[str] = []

    BLOCKS = [Restricao, ValoresSeriePatamar]

    @property
    def restricao(self) -> Optional[int]:
        """
        A restrição associada ao arquivo lido.

        :return: O código da restrição
        :rtype: int
        """
        b = self.data.get_blocks_of_type(Restricao)
        if isinstance(b, Restricao):
            return b.data
        return None
