from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie import _ArquivoSerieBase
from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.blocos.valoresserie import ValoresSerie


class ArquivoSubmercado(_ArquivoSerieBase):
    """
    Armazena os dados das saídas por submercado.
    """

    __slots__: list[str] = []

    BLOCKS = [Submercado, ValoresSerie]

    @property
    def submercado(self) -> Optional[str]:
        """
        O submercado associado ao arquivo lido.

        :return: Os nome do submercado
        :rtype: str
        """
        b = self.data.get_blocks_of_type(Submercado)
        if isinstance(b, Submercado):
            return b.data
        return None
