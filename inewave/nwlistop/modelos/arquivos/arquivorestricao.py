from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie import _ArquivoSerieBase
from inewave.nwlistop.modelos.blocos.restricao import Restricao
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class ArquivoRestricao(_ArquivoSerieBase):
    """
    Armazena os dados das saídas por usina.
    """

    __slots__: list[str] = []

    BLOCKS = [Restricao, ValoresSerie]

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
