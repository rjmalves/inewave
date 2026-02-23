from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie import _ArquivoSerieBase
from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class ArquivoUsina(_ArquivoSerieBase):
    """
    Armazena os dados das saídas por usina.
    """

    __slots__: list[str] = []

    BLOCKS = [Usina, ValoresSerie]

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
