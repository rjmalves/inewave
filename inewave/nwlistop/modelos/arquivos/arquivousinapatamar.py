from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie_patamar import (
    _ArquivoSeriePatamarBase,
)
from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class ArquivoUsinaPatamar(_ArquivoSeriePatamarBase):
    """
    Armazena os dados das saídas por patamar, por Usina.
    """

    __slots__: list[str] = []

    BLOCKS = [Usina, ValoresSeriePatamar]

    @property
    def usina(self) -> Optional[str]:
        """
        A usina associada ao arquivo lido.

        :return: O nome da usina
        :rtype: str
        """
        b = self.data.get_blocks_of_type(Usina)
        if isinstance(b, Usina):
            return b.data
        return None
