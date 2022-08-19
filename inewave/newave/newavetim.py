from inewave.newave.modelos.newavetim import BlocoTemposEtapasTim

from cfinterface.components.block import Block
from cfinterface.files.blockfile import BlockFile
from typing import Type, TypeVar, Optional, Any
import pandas as pd  # type: ignore


class NewaveTim(BlockFile):
    """
    Armazena os dados de saída do NEWAVE referentes aos
    tempos de execução do programa.

    """

    T = TypeVar("T")

    BLOCKS = [BlocoTemposEtapasTim]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="newave.tim"
    ) -> "NewaveTim":
        return cls.read(diretorio, nome_arquivo)

    def __bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
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

    def __extrai_dados_se_existe(
        self, bloco: Type[Block], indice: int = 0
    ) -> Optional[Any]:
        """
        Obtém os dados de um bloco se este existir dentre os blocos do arquivo.

        :param bloco: O tipo do bloco cujos dados serão extraídos
        :type bloco: Type[T]
        :param indice: Qual dos blocos do tipo será acessado
        :type indice: int, optional
        :return: Os dados do bloco, se existirem
        :rtype: Any
        """
        b = self.__bloco_por_tipo(bloco, indice)
        if b is not None:
            return b.data
        return None

    @property
    def tempos_etapas(self) -> Optional[pd.DataFrame]:
        """
        Tempos de execução do modelo por etapa do modelo.

        - Etapa (`str`)
        - Tempo (`timedelta`)

        :return: Os tempos em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        return self.__extrai_dados_se_existe(BlocoTemposEtapasTim)
