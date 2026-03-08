from typing import Optional

from inewave.nwlistop.modelos.arquivos._base_serie_patamar import (
    _ArquivoSeriePatamarBase,
)
from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.blocos.tabela_serie_patamar_anual import (
    TabelaSeriePatamarAnual,
)
from inewave.nwlistop.modelos.blocos.valoresclassetermicaseriepatamar import (
    ValoresClasseTermicaSeriePatamar,
)


class ArquivoClasseTermicaSubmercadoPatamar(_ArquivoSeriePatamarBase):
    """
    Armazena os dados das saídas por patamar, por submercado e por
    classe térmica.
    """

    __slots__: list[str] = []

    _DATA_BLOCK_TYPES = (
        ValoresClasseTermicaSeriePatamar,
        TabelaSeriePatamarAnual,
    )

    BLOCKS = [Submercado, ValoresClasseTermicaSeriePatamar]

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
