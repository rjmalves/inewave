from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie_patamar import (
    _ArquivoSeriePatamarBase,
)
from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class ArquivoREEPatamar(_ArquivoSeriePatamarBase):
    """
    Armazena os dados das saídas por patamar, por REE.
    """

    __slots__: list[str] = []

    BLOCKS = [REE, ValoresSeriePatamar]

    @property
    def ree(self) -> Optional[str]:
        """
        O REE associado ao arquivo lido.

        :return: O nome do REE
        :rtype: str
        """
        b = self.data.get_blocks_of_type(REE)
        if isinstance(b, REE):
            return b.data
        return None
