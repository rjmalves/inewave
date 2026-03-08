from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie import _ArquivoSerieBase
from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class ArquivoREE(_ArquivoSerieBase):
    """
    Armazena os dados das saídas por REE.
    """

    __slots__: list[str] = []

    BLOCKS = [REE, ValoresSerie]

    @property
    def ree(self) -> Optional[str]:
        """
        O REE associado ao arquivo lido.

        :return: O nome do ree
        :rtype: str
        """
        b = self.data.get_blocks_of_type(REE)
        if isinstance(b, REE):
            return b.data
        return None
