from inewave.nwlistop.modelos.verturbsin import VertAnos

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import Type, TypeVar, Optional


class VerturbSIN(BlockFile):
    """
    Armazena os dados das saídas referentes às energias
    vertidas para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `verturbsin.out`.

    """

    T = TypeVar("T")

    BLOCKS = [
        VertAnos,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__earms = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="verturbsin.out"
    ) -> "VerturbSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="verturbsin.out"):
        self.write(diretorio, nome_arquivo)

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

    def __monta_tabela(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(VertAnos):
            dados = b.data
            if dados is None:
                continue
            elif df is None:
                df = b.data
            else:
                df = pd.concat([df, b.data], ignore_index=True)
        return df

    @property
    def vertimentos(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as energias vertidas por série e
        por mês/ano de estudo.

        :return: A tabela das energias vertidas.
        :rtype: Optional[pd.DataFrame]
        """
        if self.__earms is None:
            self.__earms = self.__monta_tabela()
        return self.__earms
