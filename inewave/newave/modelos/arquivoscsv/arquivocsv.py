from inewave.newave.modelos.blocos.versaomodelo import VersaoModelo
from inewave.newave.modelos.blocos.tabelacsv import TabelaCSV

from cfinterface.components.block import Block
from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import List, Type, TypeVar, Optional


class ArquivoCSV(BlockFile):
    """
    Modelo de arquivo baseado em blocos específico para o formato
    dos arquivos de saída .CSV do NEWAVE. Espera conter
    a implementação de dois blocos específicos:

    - Versão do modelo
    - Tabela de dados

    O primeiro é genérico, mas o segundo deve ser
    implementado para cada arquivo específico a ser lido.
    """

    BLOCKS: List[Type[Block]] = [VersaoModelo]
    ENCODING = "iso-8859-1"

    T = TypeVar("T")

    @property
    def versao(self) -> Optional[str]:
        """
        A versão do modelo utilizada para executar o caso.

        :return: A versão do modelo
        :rtype: str | None
        """
        b = self.data.get_blocks_of_type(VersaoModelo)
        if isinstance(b, VersaoModelo):
            return b.data
        return None

    def _tabela(self) -> Optional[pd.DataFrame]:
        """
        A tabela de dados que está contida no arquivo.

        :return: A tabela como um dataframe
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(TabelaCSV)
        if isinstance(b, TabelaCSV):
            return b.data
        return None
