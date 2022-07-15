from inewave.nwlistop.modelos.vertuh import Usina, VertAnos

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import Type, TypeVar, Optional


class VertUH(BlockFile):
    """
    Armazena os dados das saídas referentes aos vertimentos por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vertuh00x.out`, onde x varia conforme a
    usina em questão.

    """

    T = TypeVar("T")

    BLOCKS = [
        Usina,
        VertAnos,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__vertuh = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vertuh001.out"
    ) -> "VertUH":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vertuh001.out"):
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
        Tabela com valores de vertimento por série e
        por mês/ano de estudo.

        - Ano (`int`)
        - Série (`int`)
        - Janeiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A tabela dos valores de vertimento.
        :rtype: pd.DataFrame
        """
        if self.__vertuh is None:
            self.__vertuh = self.__monta_tabela()
        return self.__vertuh

    @property
    def usina(self) -> Optional[str]:
        """
        A usina associada ao arquivo lido.

        :return: O nome da usina
        :rtype: str
        """
        b = self.__bloco_por_tipo(Usina, 0)
        if b is not None:
            return b.data
        return None
