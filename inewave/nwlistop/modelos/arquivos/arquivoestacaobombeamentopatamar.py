from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie_patamar import (
    _ArquivoSeriePatamarBase,
)
from inewave.nwlistop.modelos.blocos.estacaobombeamento import (
    EstacaoBombeamento,
)
from inewave.nwlistop.modelos.blocos.valoresseriepatamar import (
    ValoresSeriePatamar,
)


class ArquivoEstacaoBombeamentoPatamar(_ArquivoSeriePatamarBase):
    """
    Armazena os dados das saídas por patamar, por Estação de Bombeamento.
    """

    __slots__: list[str] = []

    BLOCKS = [EstacaoBombeamento, ValoresSeriePatamar]

    @property
    def estacao(self) -> Optional[str]:
        """
        A estação associada ao arquivo lido.

        :return: O nome da estação
        :rtype: str
        """
        b = self.data.get_blocks_of_type(EstacaoBombeamento)
        if isinstance(b, EstacaoBombeamento):
            return b.data
        return None
