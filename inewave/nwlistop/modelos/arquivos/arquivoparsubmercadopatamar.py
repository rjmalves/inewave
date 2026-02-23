from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie_patamar import (
    _ArquivoSeriePatamarBase,
)
from inewave.nwlistop.modelos.blocos.parsubmercados import ParSubmercados
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class ArquivoParSubmercadoPatamar(_ArquivoSeriePatamarBase):
    """
    Armazena os dados das saídas por patamar, por par de submercados.
    """

    __slots__: list[str] = []

    BLOCKS = [ParSubmercados, ValoresSeriePatamar]

    @property
    def submercado_de(self) -> Optional[str]:
        """
        O submercado de origem associado ao arquivo lido.

        :return: Os nome do submercado
        :rtype: str
        """
        b = self.data.get_blocks_of_type(ParSubmercados)
        if isinstance(b, ParSubmercados):
            return b.data[0]
        return None

    @property
    def submercado_para(self) -> Optional[str]:
        """
        O submercado de destino associado ao arquivo lido.

        :return: Os nome do submercado
        :rtype: str
        """
        b = self.data.get_blocks_of_type(ParSubmercados)
        if isinstance(b, ParSubmercados):
            return b.data[1]
        return None
