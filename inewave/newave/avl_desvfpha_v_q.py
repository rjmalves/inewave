from inewave.newave.modelos.blocos.versaomodelo import VersaoModelo
from inewave.newave.modelos.avl_desvfpha_v_q import TabelaAvlDesvFphaVQ

from cfinterface.files.blockfile import BlockFile
from typing import Optional, TypeVar, Type
import pandas as pd  # type: ignore


class AvlDesvFphaVQ(BlockFile):
    """
    Arquivo com os desvios da função de produção nos planos de
    volume armazenado e vazão turbinada (V-Q).
    """

    BLOCKS = [VersaoModelo, TabelaAvlDesvFphaVQ]
    ENCODING = "iso-8859-1"

    T = TypeVar("T")

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__df_completo: Optional[pd.DataFrame] = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, arquivo: str = "avl_desvfpha_v_q_001.dat"
    ) -> "AvlDesvFphaVQ":
        return cls.read(diretorio, arquivo)

    @property
    def tabela(self) -> Optional[pd.DataFrame]:
        """
        A tabela de dados que está contida no arquivo.

        - indice_usina (`int`)
        - nome_usina (`str`)
        - volume_armazenado_percentual (`float`)
        - vazao_turbinada_m3s (`float`)
        - desvio_percentual (`float`)

        :return: A tabela como um dataframe
        :rtype: pd.DataFrame | None
        """
        if self.__df_completo is None:
            tabelas = self.data.of_type(TabelaAvlDesvFphaVQ)
            self.__df_completo = pd.DataFrame()
            for t in tabelas:
                self.__df_completo = pd.concat(
                    [self.__df_completo, t.data], ignore_index=True
                )
        return self.__df_completo

    def _bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int
        :return: O gerador de blocos, se houver
        :rtype: Optional[Generator[T], None, None]
        """
        try:
            return next(
                b
                for i, b in enumerate(self.data.of_type(bloco))
                if i == indice
            )
        except StopIteration:
            return None

    @property
    def versao(self) -> Optional[str]:
        """
        A versão do modelo utilizada para executar o caso.

        :return: A versão do modelo
        :rtype: str | None
        """
        b = self._bloco_por_tipo(VersaoModelo, 0)
        if b is not None:
            return b.data
        return None
